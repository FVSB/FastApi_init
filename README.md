
# 📚 FastAPI Books & Tags API

API REST desarrollada con **FastAPI** y **PostgreSQL** para gestionar libros y etiquetas. Proyecto educativo que demuestra implementación CRUD, relaciones many-to-many y mejores prácticas.

## 🎯 Propósito

**Caso de ejemplo** para aprender:
- Arquitectura modular con FastAPI
- Operaciones CRUD asíncronas
- Relaciones many-to-many (Books ↔ Tags)
- SQLModel + PostgreSQL
- Testing con pytest
- Contenerización con Docker

---

## 🏗️ Arquitectura

```
src/
├── books/          # Módulo libros (routes, schemas, service)
├── tags/           # Módulo tags (routes, schemas, service)
├── db/             # Modelos y conexión DB
├── utils/          # Manejo de errores
├── config.py       # Configuración
└── main.py         # App principal
```

**Stack Tecnológico:**
- FastAPI 0.116.1 + SQLModel 0.0.24
- PostgreSQL 15 + Asyncpg
- Alembic (migraciones)
- pytest + Docker

---

## 📊 Modelos de Datos

### Book
```python
id: int (PK)
title: str (unique, max 100)
author: str (max 100)
publisher: str
published_date: date
page_count: int
language_code: str (max 5)
created_at, update_at: datetime
tags: List[Tag]  # many-to-many
```

### Tag
```python
id: int (PK)
name: str (unique, max 100)
created_at: datetime
books: List[Book]  # many-to-many
```

---

## 🔌 API Endpoints

**Base URL:** `http://localhost:8000/api/v1`

### 📖 Books
```http
GET    /books/                    # Listar libros (?with_tags=true)
GET    /books/books/{id}          # Obtener libro
POST   /books/books               # Crear libro
PUT    /books/books/{id}          # Actualizar libro
DELETE /books/books/{id}          # Eliminar libro
```

### 🏷️ Tags
```http
GET    /tags/                     # Listar tags
POST   /tags/                     # Crear tag
PUT    /tags/{id}                 # Actualizar tag
DELETE /tags/{id}                 # Eliminar tag
POST   /tags/book/{id}/tags       # Añadir tags a libro
```

### Ejemplo de Request/Response

**POST** `/books/books`
```json
{
  "title": "Cien años de soledad",
  "author": "Gabriel García Márquez",
  "publisher": "Sudamericana",
  "published_date": "1967-05-30",
  "page_count": 471,
  "language_code": "es",
  "created_at": "2024-01-15T10:30:00",
  "update_at": "2024-01-15T10:30:00"
}
```

**Response** `201 Created`:
```json
{
  "id": 1,
  "title": "Cien años de soledad",
  "author": "Gabriel García Márquez",
  "tags": [
    {"id": 1, "name": "Realismo Mágico", "created_at": "2024-01-15T09:00:00"}
  ]
}
```

---

## 🚀 Instalación y Ejecución

### Opción 1: Docker Compose (Recomendado)

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd FastApi_init

# 2. Crear .env
cat > .env << EOF
POSTGRES_USER=postgres
POSTGRES_DB=bookdb
POSTGRES_PASSWORD=postgres123
DATABASE_URL=postgresql+asyncpg://postgres:postgres123@db:5432/bookdb
DATABASE_MIGRATIONS_URL=postgresql://postgres:postgres123@db:5432/bookdb
EOF

# 3. Levantar servicios
docker-compose up -d

# 4. Ejecutar migraciones
docker-compose exec app alembic upgrade head
```

### Opción 2: Local

```bash
# 1. Preparar entorno
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configurar PostgreSQL y variables de entorno
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/bookdb"
export DATABASE_MIGRATIONS_URL="postgresql://user:pass@localhost:5432/bookdb"

# 3. Migraciones y ejecutar
alembic upgrade head
python src/main.py
```

### Acceso
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Testing
```bash
pytest                    # Todas las pruebas
pytest --cov=src         # Con cobertura
pytest test/test_*.py    # Pruebas específicas
```

---

## 🛠️ Mejoras Sugeridas (Caso de Estudio)

### ✅ Implementado
- ✓ CRUD completo asíncrono
- ✓ Validación con Pydantic
- ✓ Relaciones many-to-many
- ✓ Documentación automática
- ✓ Testing básico
- ✓ Contenerización

### 🔧 Oportunidades de Mejora

#### 1. **Autenticación & Seguridad**
```python
# TODO: JWT authentication
from fastapi.security import HTTPBearer
# TODO: Role-based access control
# TODO: Rate limiting
```

#### 2. **Performance & Escalabilidad**
```python
# TODO: Paginación en endpoints
@router.get("/books/")
async def get_books(page: int = 1, size: int = 10):
    # Implementar offset/limit

# TODO: Cache con Redis
# TODO: Connection pooling optimizado
# TODO: Índices de DB optimizados
```

#### 3. **Observabilidad**
```python
# TODO: Logging estructurado
import structlog
# TODO: Métricas (Prometheus)
# TODO: Health checks
# TODO: Distributed tracing
```

#### 4. **Validaciones de Negocio**
```python
# TODO: Validaciones más robustas
@validator('published_date')
def validate_date(cls, v):
    if v > date.today():
        raise ValueError('No puede ser futuro')
    return v
```

#### 5. **Testing Avanzado**
```python
# TODO: Integration tests
# TODO: Property-based testing (Hypothesis)
# TODO: Load testing (Locust)
# TODO: Contract testing
```

### 🚀 Roadmap Sugerido
1. **Auth JWT** → Seguridad básica
2. **Cache Redis** → Performance
3. **Búsqueda Full-text** → Elasticsearch
4. **Real-time** → WebSockets
5. **Microservices** → Event-driven architecture

---

## 📝 Contribuir

1. Fork → `git checkout -b feature/nueva-funcionalidad`
2. Commit → `git commit -am 'Add feature'`
3. Push → `git push origin feature/nueva-funcionalidad`
4. Pull Request

**Licencia:** MIT | **Autor:** Proyecto educativo FastAPI + PostgreSQL
