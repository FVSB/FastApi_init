"""
Simple unit tests for BookService
These tests are straightforward and easy to understand, mocking only what is necessary.
"""

import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime, date
from src.books.service import BookService
from src.books.schemas import BookCreateModel, BookUpdateModel
from src.db.models import Book, Tag
from src.utils.errors import BookNotFound


class TestBookServiceSimple:
    """Tests unitarios simples para BookService"""

    @pytest.fixture
    def book_service(self):
        """Instancia del servicio para testing"""
        return BookService()

    @pytest.fixture
    def mock_session(self):
        """Sesión de BD mockeada"""
        return AsyncMock()

    @pytest.fixture
    def sample_book(self):
        """Libro de ejemplo para tests"""
        return Book(
            id=1,
            title="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            published_date=date(2024, 1, 1),
            page_count=200,
            language_code="es",
            created_at=datetime(2024, 1, 1, 10, 0, 0),
            update_at=datetime(2024, 1, 1, 10, 0, 0),
            tags=[]
        )

    # ==================== TESTS GET_ALL_BOOKS ====================
    
    async def test_get_all_books_with_tags_true(self, book_service, mock_session, sample_book):
        """Test simple: obtener todos los libros CON tags"""
        # Arrange - Preparar datos falsos
        sample_book.tags = [Tag(id=1, name="Fiction", created_at=datetime.now())]
        
        mock_result = Mock()
        mock_result.all.return_value = [sample_book]
        mock_session.exec.return_value = mock_result

        # Act - Ejecutar
        result = await book_service.get_all_books(mock_session, with_tags=True)

        # Assert - Verificar
        assert len(result) == 1
        assert result[0].title == "Test Book"
        assert len(result[0].tags) == 1
        mock_session.exec.assert_called_once()

    async def test_get_all_books_with_tags_false(self, book_service, mock_session, sample_book):
        """Test simple: obtener todos los libros SIN tags"""
        # Arrange - Preparar datos falsos (sin tags)
        sample_book.tags = []
        
        mock_result = Mock()
        mock_result.all.return_value = [sample_book]
        mock_session.exec.return_value = mock_result

        # Act - Ejecutar
        result = await book_service.get_all_books(mock_session, with_tags=False)

        # Assert - Verificar
        assert len(result) == 1
        assert result[0].title == "Test Book"
        assert result[0].tags == []
        mock_session.exec.assert_called_once()

    async def test_get_all_books_empty_database(self, book_service, mock_session):
        """Test simple: BD vacía"""
        # Arrange
        mock_result = Mock()
        mock_result.all.return_value = []
        mock_session.exec.return_value = mock_result

        # Act
        result = await book_service.get_all_books(mock_session)

        # Assert
        assert len(result) == 0
        mock_session.exec.assert_called_once()

    # ==================== TESTS GET_BOOK_OR_404 ====================

    async def test_get_book_or_404_found(self, book_service, mock_session, sample_book):
        """Test simple: libro encontrado"""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_book
        mock_session.exec.return_value = mock_result

        # Act
        result = await book_service.get_book_or_404(1, mock_session)

        # Assert
        assert result.id == 1
        assert result.title == "Test Book"
        mock_session.exec.assert_called_once()

    async def test_get_book_or_404_not_found(self, book_service, mock_session):
        """Test simple: libro NO encontrado - debe lanzar excepción"""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = None  # Simula libro no encontrado
        mock_session.exec.return_value = mock_result

        # Act & Assert
        with pytest.raises(BookNotFound):
            await book_service.get_book_or_404(999, mock_session)

    # ==================== TESTS CREATE_BOOK ====================

    async def test_create_book_simple(self, book_service, mock_session):
       
        # Arrange
        book_data = BookCreateModel(
            title="Nuevo Libro",
            author="Nuevo Autor",
            publisher="Nueva Editorial",
            published_date="2024-01-15",
            page_count=300,
            language_code="es",
            created_at=datetime(2024, 1, 1, 10, 0, 0),
            update_at=datetime(2024, 1, 1, 10, 0, 0)
        )

        # Act
        result = await book_service.create_book(book_data, mock_session)

        # Assert
        assert result.title == "Nuevo Libro"
        assert result.author == "Nuevo Autor"
        assert result.page_count == 300
        
        

    # ==================== TESTS UPDATE_BOOK ====================

    async def test_update_book_success(self, book_service, mock_session, sample_book):
        """Test simple: actualizar libro existente"""
        # Arrange
        update_data = BookUpdateModel(
            title="Título Actualizado",
            author="Autor Actualizado",
            publisher="Editorial Actualizada",
            published_date="2024-02-15",
            page_count=350,
            language_code="en",
            created_at=datetime(2024, 2, 15, 10, 0, 0),
            update_at=datetime(2024, 2, 15, 10, 0, 0)
        )

        # Mock get_book_or_404 para que devuelva el libro
        mock_result = Mock()
        mock_result.first.return_value = sample_book
        mock_session.exec.return_value = mock_result

        # Act
        result = await book_service.update_book(1, update_data, mock_session)

        # Assert
        assert result.title == "Título Actualizado"
        assert result.author == "Autor Actualizado"
        assert result.page_count == 350
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    # ==================== TESTS DELETE_BOOK ====================

    async def test_delete_book_success(self, book_service, mock_session, sample_book):
        """Test simple: eliminar libro existente"""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_book
        mock_session.exec.return_value = mock_result

        # Act
        result = await book_service.delete_book(1, mock_session)

        # Assert
        assert result == {}  # Método retorna dict vacío
        mock_session.delete.assert_called_once_with(sample_book)
        mock_session.commit.assert_called_once()

    async def test_delete_book_not_found(self, book_service, mock_session):
        """Test simple: eliminar libro que no existe"""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = None
        mock_session.exec.return_value = mock_result

        # Act & Assert
        with pytest.raises(BookNotFound):
            await book_service.delete_book(999, mock_session)


# ==================== TEST EJECUTOR ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
