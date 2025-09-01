"""
Simple unit tests for TagService
These tests are straightforward and easy to understand, mocking only what's necessary.
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime
from fastapi import HTTPException
from src.tags.service import TagService
from src.tags.schemas import TagCreateModel, TagAddModel
from src.db.models import Tag, Book
from src.utils.errors import TagNotFound, TagAlreadyExists, BookNotFound


class TestTagServiceSimple:
    """Simple unit tests for TagService"""

    @pytest.fixture
    def tag_service(self):
        """Service instance for testing"""
        return TagService()

    @pytest.fixture
    def mock_session(self):
        """Mocked database session"""
        return AsyncMock()

    @pytest.fixture
    def sample_tag(self):
        """Sample tag for testing"""
        return Tag(
            id=1,
            name="Fiction",
            created_at=datetime(2024, 1, 1, 10, 0, 0)
        )

    @pytest.fixture
    def sample_book(self):
        """Sample book for testing"""
        return Book(
            id=1,
            title="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            published_date=datetime(2024, 1, 1).date(),
            page_count=200,
            language_code="es",
            created_at=datetime(2024, 1, 1, 10, 0, 0),
            update_at=datetime(2024, 1, 1, 10, 0, 0),
            tags=[]
        )

    # ==================== TESTS GET_TAGS ====================
    
    async def test_get_tags_with_results(self, tag_service, mock_session, sample_tag):
        """Simple test: get all tags when data exists"""
        # Arrange
        mock_result = Mock()
        mock_result.all.return_value = [sample_tag]
        mock_session.exec.return_value = mock_result

        # Act
        result = await tag_service.get_tags(mock_session)

        # Assert
        assert len(result) == 1
        assert result[0].name == "Fiction"
        assert result[0].id == 1
        mock_session.exec.assert_called_once()

    async def test_get_tags_empty_database(self, tag_service, mock_session):
        """Simple test: get tags when database is empty"""
        # Arrange
        mock_result = Mock()
        mock_result.all.return_value = []
        mock_session.exec.return_value = mock_result

        # Act
        result = await tag_service.get_tags(mock_session)

        # Assert
        assert len(result) == 0
        mock_session.exec.assert_called_once()

    # ==================== TESTS GET_TAG_BY_UID ====================

    async def test_get_tag_by_uid_found(self, tag_service, mock_session, sample_tag):
        """Simple test: get tag by ID when it exists"""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_tag
        mock_session.exec.return_value = mock_result

        # Act
        result = await tag_service.get_tag_by_uid(1, mock_session)

        # Assert
        assert result.id == 1
        assert result.name == "Fiction"
        mock_session.exec.assert_called_once()

    async def test_get_tag_by_uid_not_found(self, tag_service, mock_session):
        """Simple test: get tag by ID when it doesn't exist"""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = None
        mock_session.exec.return_value = mock_result

        # Act
        result = await tag_service.get_tag_by_uid(999, mock_session)

        # Assert
        assert result is None
        mock_session.exec.assert_called_once()

    # ==================== TESTS ADD_TAG ====================

    async def test_add_tag_success(self, tag_service, mock_session):
        """Simple test: create new tag successfully"""
        # Arrange
        tag_data = TagCreateModel(name="New Tag")
        
        # Mock to verify tag doesn't exist
        mock_result = Mock()
        mock_result.first.return_value = None  # Tag doesn't exist
        mock_session.exec.return_value = mock_result

        # Act
        result = await tag_service.add_tag(tag_data, mock_session)

        # Assert
        assert result.name == "New Tag"
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    async def test_add_tag_already_exists(self, tag_service, mock_session, sample_tag):
        """Simple test: create tag that already exists - should raise exception"""
        # Arrange
        tag_data = TagCreateModel(name="Fiction")
        
        # Mock to simulate tag already exists
        mock_result = Mock()
        mock_result.first.return_value = sample_tag  # Tag already exists
        mock_session.exec.return_value = mock_result

        # Act & Assert
        with pytest.raises(TagAlreadyExists):
            await tag_service.add_tag(tag_data, mock_session)

    # ==================== TESTS UPDATE_TAG ====================

    async def test_update_tag_success(self, tag_service, mock_session, sample_tag):
        """Simple test: update existing tag"""
        # Arrange
        update_data = TagCreateModel(name="Updated Fiction")
        
        # Mock get_tag_by_uid to return the tag
        with patch.object(tag_service, 'get_tag_by_uid', return_value=sample_tag):
            # Act
            result = await tag_service.update_tag(1, update_data, mock_session)

            # Assert
            assert result.name == "Updated Fiction"
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once()

    async def test_update_tag_not_found(self, tag_service, mock_session):
        """Simple test: update tag that doesn't exist"""
        # Arrange
        update_data = TagCreateModel(name="Non Existing")
        
        # Mock get_tag_by_uid to return None
        with patch.object(tag_service, 'get_tag_by_uid', return_value=None):
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                await tag_service.update_tag(999, update_data, mock_session)
            
            assert exc_info.value.status_code == 404

    # ==================== TESTS DELETE_TAG ====================

    async def test_delete_tag_success(self, tag_service, mock_session, sample_tag):
        """Simple test: delete existing tag"""
        # Arrange
        # Mock get_tag_by_uid to return the tag
        with patch.object(tag_service, 'get_tag_by_uid', return_value=sample_tag):
            # Act
            await tag_service.delete_tag(1, mock_session)

            # Assert
            mock_session.delete.assert_called_once_with(sample_tag)
            mock_session.commit.assert_called_once()

    async def test_delete_tag_not_found(self, tag_service, mock_session):
        """Simple test: delete tag that doesn't exist"""
        # Arrange
        # Mock get_tag_by_uid to return None
        with patch.object(tag_service, 'get_tag_by_uid', return_value=None):
            # Act & Assert
            with pytest.raises(TagNotFound):
                await tag_service.delete_tag(999, mock_session)

    # ==================== TESTS ADD_TAGS_TO_BOOK ====================

    async def test_add_tags_to_book_success(self, tag_service, mock_session, sample_book):
        """Simple test: add tags to existing book"""
        # Arrange
        tag_data = TagAddModel(tags=[
            TagCreateModel(name="Fiction"),
            TagCreateModel(name="Adventure")
        ])
        
        # Mock for book_service.get_book_or_404
        with patch('src.tags.service.book_service.get_book_or_404', return_value=sample_book):
            # Mock to verify existing tags
            mock_result = Mock()
            mock_result.one_or_none.return_value = None  # Tags don't exist
            mock_session.exec.return_value = mock_result

            # Act
            result = await tag_service.add_tags_to_book(1, tag_data, mock_session)

            # Assert
            assert result == sample_book
            assert len(sample_book.tags) == 2  # 2 tags were added
            mock_session.add.assert_called_once_with(sample_book)
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once()

    async def test_add_tags_to_book_not_found(self, tag_service, mock_session):
        """Simple test: add tags to book that doesn't exist"""
        # Arrange
        tag_data = TagAddModel(tags=[TagCreateModel(name="Fiction")])
        
        # Mock for book_service.get_book_or_404 to raise exception
        with patch('src.tags.service.book_service.get_book_or_404', side_effect=BookNotFound()):
            # Act & Assert
            with pytest.raises(BookNotFound):
                await tag_service.add_tags_to_book(999, tag_data, mock_session)

    async def test_add_existing_tags_to_book(self, tag_service, mock_session, sample_book, sample_tag):
        """Simple test: add existing tags to a book"""
        # Arrange
        tag_data = TagAddModel(tags=[TagCreateModel(name="Fiction")])
        
        # Mock for book_service.get_book_or_404
        with patch('src.tags.service.book_service.get_book_or_404', return_value=sample_book):
            # Mock to find existing tag
            mock_result = Mock()
            mock_result.one_or_none.return_value = sample_tag  # Tag already exists
            mock_session.exec.return_value = mock_result

            # Act
            result = await tag_service.add_tags_to_book(1, tag_data, mock_session)

            # Assert
            assert result == sample_book
            assert sample_tag in sample_book.tags  # Existing tag was added
            mock_session.add.assert_called_once_with(sample_book)
            mock_session.commit.assert_called_once()


# ==================== TEST RUNNER ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
