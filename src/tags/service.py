from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.service import BookService
from src.db.models import Tag

from .schemas import TagAddModel, TagCreateModel
from src.utils.errors import BookNotFound, TagNotFound, TagAlreadyExists

book_service = BookService()


server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong"
)


class TagService:

    async def get_tags(self, session: AsyncSession):
        """
        Retrieve all tags from the database.

        Args:
            session (AsyncSession): Database session for executing queries.

        Returns:
            Sequence[Tag]: All tags ordered by creation date (newest first).

        Note:
            Uses descending order by created_at for consistent chronological listing.
        """

        statement = select(Tag).order_by(desc(Tag.created_at))

        result = await session.exec(statement)

        return result.all()

    async def add_tags_to_book(
        self, book_id: int, tag_data: TagAddModel, session: AsyncSession
    ):
        """
        Add multiple tags to a specific book.

        Args:
            book_id (int): The unique identifier of the book (Autoincrement).
            tag_data (TagAddModel): Contains list of tags to add to the book.
            session (AsyncSession): Database session for executing the transaction.

        Returns:
            Book: The updated book with all associated tags.

        Raises:
            BookNotFound: If no book exists with the given ID.

        Note:
            Creates new tags automatically if they don't exist.
            Avoids duplicate tags by checking existing names first.
            Refreshes book instance to include all current relationships.
        """

        book = await book_service.get_book_or_404(book_id=book_id, session=session)

        if not book:
            raise BookNotFound()

        for tag_item in tag_data.tags:
            result = await session.exec(select(Tag).where(Tag.name == tag_item.name))

            tag = result.one_or_none()
            
            if not tag:
                tag = Tag(name=tag_item.name)

            book.tags.append(tag)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def get_tag_by_uid(self, tag_id: int, session: AsyncSession):
        
        """
        Retrieve a specific tag by its ID.

        Args:
            tag_id (int): The unique identifier of the tag.
            session (AsyncSession): Database session for executing queries.

        Returns:
            Tag | None: The requested tag if found, None otherwise.

        Note:
            Returns None instead of raising exception when tag not found.
            Use this when you need to handle missing tags gracefully.
        """
        statement = select(Tag).where(Tag.id == tag_id)

        result = await session.exec(statement)

        return result.first()

    async def add_tag(self, tag_data: TagCreateModel, session: AsyncSession):
        
        """
        Create a new tag in the database.

        Args:
            tag_data (TagCreateModel): Tag information containing the name.
            session (AsyncSession): Database session for executing the transaction.

        Returns:
            Tag: The newly created tag instance.

        Raises:
            TagAlreadyExists: If a tag with the same name already exists.

        Note:
            Enforces unique tag names by checking for duplicates before creation.
            Tag names must be unique across the entire system.
        """
        statement = select(Tag).where(Tag.name == tag_data.name)

        result = await session.exec(statement)

        tag = result.first()

        if tag:
            raise TagAlreadyExists()
        new_tag = Tag(name=tag_data.name)

        session.add(new_tag)

        await session.commit()

        return new_tag

    async def update_tag(
        self, tag_uid, tag_update_data: TagCreateModel, session: AsyncSession
    ):
        """
        Update an existing tag with new data.

        Args:
            tag_uid: The unique identifier of the tag to update.
            tag_update_data (TagCreateModel): New tag data to apply.
            session (AsyncSession): Database session for executing the transaction.

        Returns:
            Tag: The updated tag instance.

        Raises:
            HTTPException: 404 if tag not found.

        Note:
            Updates all provided fields dynamically using setattr.
            Refreshes the instance after commit to get updated values.
        """

        tag = await self.get_tag_by_uid(tag_uid, session)

        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        update_data_dict = tag_update_data.model_dump()

        for k, v in update_data_dict.items():
            setattr(tag, k, v)

        await session.commit()

        await session.refresh(tag)

        return tag

    async def delete_tag(self, tag_id: int, session: AsyncSession):
        """
        Delete a tag from the database by its ID.

        Args:
            tag_id (int): The unique identifier of the tag to delete.
            session (AsyncSession): Database session for executing the transaction.

        Returns:
            None: No return value after successful deletion.

        Raises:
            TagNotFound: If no tag exists with the given ID.

        Note:
            Permanently removes the tag and commits the transaction.
            Consider cascade effects on book-tag relationships.
        """
        tag = await self.get_tag_by_uid(tag_id, session)

        if not tag:
            raise TagNotFound()

        await session.delete(tag)

        await session.commit()
