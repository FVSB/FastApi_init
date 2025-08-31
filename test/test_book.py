import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.books.schemas import BookCreateModel, BookUpdateModel
from src.db.models import Book
from datetime import datetime, date
import uuid

books_prefix = "/api/v1/books"


class TestBookAPI:
    """Clase para agrupar todas las pruebas de la API de libros"""

    def test_get_all_books(self, test_client, fake_session):
        """Prueba para obtener todos los libros"""
        with patch('src.books.routes.book_service.get_all_books', new_callable=AsyncMock) as mock_get_all:
            mock_get_all.return_value = []
            
            response = test_client.get(url=books_prefix)
            
            # Verificar que se llamó al servicio
            mock_get_all.assert_called_once_with(fake_session)
            assert response.status_code == 200

    def test_create_book(self, test_client, fake_session):
        """Prueba para crear un nuevo libro"""
        # Datos de prueba
        book_data = {
            "title": "Test Title",
            "author": "Test Author",
            "publisher": "Test Publications",
            "published_date": "2024-12-10",
            "language_code": "En",
            "page_count": 215
        }
        
        # Mock del libro creado
        mock_book = Book(
            uid=uuid.uuid4(),
            title=book_data["title"],
            author=book_data["author"],
            publisher=book_data["publisher"],
            published_date=date(2024, 12, 10),
            language_code=book_data["language_code"],
            page_count=book_data["page_count"],
            created_at=datetime.now(),
            update_at=datetime.now()
        )
        
        with patch('src.books.routes.book_service.create_book', new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_book
            
            response = test_client.post(
                url=books_prefix,
                json=book_data
            )
            
            # Verificar que se llamó al servicio
            mock_create.assert_called_once()
            call_args = mock_create.call_args
            
            
            assert response.status_code == 201

    def test_get_book_by_uid(self, test_client, fake_session):
        """Prueba para obtener un libro por su UID"""
        book_uid = str(uuid.uuid4())
        
        # Mock del libro
        mock_book = Book(
            uid=uuid.UUID(book_uid),
            title="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            published_date=date(2024, 1, 1),
            language_code="En",
            page_count=200,
            created_at=datetime.now(),
            update_at=datetime.now()
        )
        
        with patch('src.books.routes.book_service.get_book', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_book
            
            response = test_client.get(f"{books_prefix}/{book_uid}")
            
            # Verificar que se llamó al servicio
            mock_get.assert_called_once_with(book_uid, fake_session)
            assert response.status_code == 200

    def test_update_book_by_uid(self, test_client, fake_session):
        """Prueba para actualizar un libro por su UID"""
        book_uid = str(uuid.uuid4())
        
        # Datos de actualización
        update_data = {
            "title": "Updated Title",
            "author": "Updated Author",
            "publisher": "Updated Publisher",
            "language_code": "Es",
            "page_count": 300
        }
        
        # Mock del libro actualizado
        mock_book = Book(
            uid=uuid.UUID(book_uid),
            title=update_data["title"],
            author=update_data["author"],
            publisher=update_data["publisher"],
            published_date=date(2024, 1, 1),
            language_code=update_data["language_code"],
            page_count=update_data["page_count"],
            created_at=datetime.now(),
            update_at=datetime.now()
        )
        
        with patch('src.books.routes.book_service.update_book', new_callable=AsyncMock) as mock_update:
            mock_update.return_value = mock_book
            
            response = test_client.put(
                f"{books_prefix}/{book_uid}",
                json=update_data
            )
            
            # Verificar que se llamó al servicio
            mock_update.assert_called_once_with(book_uid, fake_session)
            assert response.status_code == 200

    def test_delete_book_by_uid(self, test_client, fake_session):
        """Prueba para eliminar un libro por su UID"""
        book_uid = str(uuid.uuid4())
        
        with patch('src.books.routes.book_service.delete_book', new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = {}
            
            response = test_client.delete(f"{books_prefix}/{book_uid}")
            
            # Verificar que se llamó al servicio
            mock_delete.assert_called_once_with(book_uid, fake_session)
            assert response.status_code == 204

    def test_get_book_not_found(self, test_client, fake_session):
        """Prueba para obtener un libro que no existe"""
        book_uid = str(uuid.uuid4())
        
        with patch('src.books.routes.book_service.get_book', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = None
            
            response = test_client.get(f"{books_prefix}/{book_uid}")
            
            # Verificar que se llamó al servicio
            mock_get.assert_called_once_with(book_uid, fake_session)
            # Verificar que se devuelve un error 404
            assert response.status_code == 404

    def test_update_book_not_found(self, test_client, fake_session):
        """Prueba para actualizar un libro que no existe"""
        book_uid = str(uuid.uuid4())
        
        update_data = {
            "title": "Updated Title",
            "author": "Updated Author",
            "publisher": "Updated Publisher",
            "language_code": "Es",
            "page_count": 300
        }
        
        with patch('src.books.routes.book_service.update_book', new_callable=AsyncMock) as mock_update:
            mock_update.return_value = None
            
            response = test_client.put(
                f"{books_prefix}/{book_uid}",
                json=update_data
            )
            
            # Verificar que se llamó al servicio
            mock_update.assert_called_once_with(book_uid, fake_session)
            # Verificar que se devuelve un error 404
            assert response.status_code == 404

    def test_delete_book_not_found(self, test_client, fake_session):
        """Prueba para eliminar un libro que no existe"""
        book_uid = str(uuid.uuid4())
        
        with patch('src.books.routes.book_service.delete_book', new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = None
            
            response = test_client.delete(f"{books_prefix}/{book_uid}")
            
            # Verificar que se llamó al servicio
            mock_delete.assert_called_once_with(book_uid, fake_session)
            # Verificar que se devuelve un error 404
            assert response.status_code == 404

