from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession



from src.books.schemas import BookModel
from src.db.main import get_session

from src.tags.schemas import TagAddModel, TagCreateModel, TagModel
from src.tags.service import TagService

from src.db.models import Book

tags_router = APIRouter()
tag_service = TagService()



@tags_router.get("/", response_model=List[TagModel])
async def get_all_tags(session: AsyncSession = Depends(get_session)):
    """
    Retrieve all tags from the database.
    
    Args:
        session (AsyncSession): Database session dependency.
    
    Returns:
        List[TagModel]: List of all tags ordered by creation date (newest first).
    
    Example:
        GET /tags
        Response: [
            {
                "id": 1,
                "name": "Fiction",
                "created_at": "2024-01-15T10:30:00"
            },
            {
                "id": 2,
                "name": "Science",
                "created_at": "2024-01-14T09:15:00"
            }
        ]
    """
    
    tags = await tag_service.get_tags(session)

    return tags


@tags_router.post(
    "/",
    response_model=TagModel,
    status_code=status.HTTP_201_CREATED,
    
)
async def add_tag(
    tag_data: TagCreateModel, session: AsyncSession = Depends(get_session)
) -> TagModel:
    """
    Create a new tag in the database.
    
    Args:
        tag_data (TagCreateModel): Tag information containing the name.
        session (AsyncSession): Database session dependency.
    
    Returns:
        TagModel: The newly created tag with id and created_at.
    
    Raises:
        422: Validation error for invalid input data.
        409: Tag already exists (if name is duplicate).
    
    Example:
        POST /tags
        {
            "name": "Science Fiction"
        }
        
        Response: 201 Created
        {
            "id": 1,
            "name": "Science Fiction",
            "created_at": "2024-01-15T10:30:00"
        }
    """

    tag_added = await tag_service.add_tag(tag_data=tag_data, session=session)

    return tag_added


@tags_router.post(
    "/book/{book_id}/tags", response_model=Book
)
async def add_tags_to_book(
    book_id: int, tag_data: TagAddModel, session: AsyncSession = Depends(get_session)
) -> Book:
    """
    Add multiple tags to a specific book.
    
    Args:
        book_id (str): The unique identifier of the book.
        tag_data (TagAddModel): List of tags to add to the book.
        session (AsyncSession): Database session dependency.
    
    Returns:
        Book: The updated book with all associated tags.
    
    Raises:
        404: Book not found.
        422: Validation error for invalid input data.
    
    Example:
        POST /book/123/tags
        {
            "tags": [
                {"name": "Fiction"},
                {"name": "Adventure"},
                {"name": "Classic"}
            ]
        }
        
        Response: Book object with updated tags list
    """

    book_with_tag = await tag_service.add_tags_to_book(
        book_id=book_id, tag_data=tag_data, session=session
    )

    return book_with_tag


@tags_router.put(
    "/{tag_id}", response_model=TagModel
)
async def update_tag(
    tag_id: str,
    tag_update_data: TagCreateModel,
    session: AsyncSession = Depends(get_session),
) -> TagModel:
    """
    Update an existing tag by its ID.
    
    Args:
        tag_id (str): The unique identifier of the tag to update.
        tag_update_data (TagCreateModel): Updated tag information (name).
        session (AsyncSession): Database session dependency.
    
    Returns:
        TagModel: The updated tag with new information.
    
    Raises:
        404: Tag not found.
        422: Validation error for invalid input data.
        409: Tag name already exists (if duplicate).
    
    Example:
        PUT /tags/123
        {
            "name": "Updated Science Fiction"
        }
        
        Response:
        {
            "id": 123,
            "name": "Updated Science Fiction",
            "created_at": "2024-01-15T10:30:00"
        }
    """
    
    updated_tag = await tag_service.update_tag(tag_id, tag_update_data, session)

    return updated_tag


@tags_router.delete(
    "/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    
)
async def delete_tag(
    tag_id: str, session: AsyncSession = Depends(get_session)
) -> None:
    """
    Delete a tag by its ID.
    
    Args:
        tag_id (str): The unique identifier of the tag to delete.
        session (AsyncSession): Database session dependency.
    
    Returns:
        None: Empty response body (204 No Content).
    
    Raises:
        404: Tag not found.
    
    Example:
        DELETE /tags/123
        Response: 204 No Content (empty body)
    """
    updated_tag = await tag_service.delete_tag(tag_id, session)

    return updated_tag
