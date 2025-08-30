# Proyecto CRUD de Libros con FastAPI y PostgreSQL

Este proyecto consiste en el desarrollo de una **aplicación CRUD sencilla** utilizando **FastAPI** como framework backend y **PostgreSQL** como base de datos.  
El objetivo es gestionar información de libros y sus reseñas (**reviews**) con persistencia en la base de datos, siguiendo buenas prácticas de desarrollo, entregando pruebas unitarias con **pytest**, y documentando el proyecto con **MkDocs**.

---

## 📚 Modelo de Datos

### Entidad **Libro**
- `title: str` → Título del libro  
- `author: str` → Autor  
- `publisher: str` → Editorial  
- `published_date: date` → Fecha de publicación  
- `page_count: int` → Número de páginas  
- `language: str` → Idioma  
- `created_at: datetime` → Fecha de creación del registro  
- `updated_at: datetime` → Última actualización del registro  

### Entidad **Review**
Un libro puede tener **0 o muchas reseñas**.  
- `rating: int = Field(lt=5)` → Valoración (0 a 4, ya que lt=5)  
- `review_text: str` → Texto de la reseña  
- `user_uid: Optional[uuid.UUID]` → Identificador del usuario que realiza la reseña  
- `book_uid: Optional[uuid.UUID]` → Identificador del libro asociado  
- `created_at: datetime` → Fecha de creación de la reseña  
- `updated_at: datetime` → Última actualización de la reseña  

---

## 🛠️ Tecnologías Requeridas

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy / SQLModel** (ORM para PostgreSQL)
- **PostgreSQL** como base de datos
- **Alembic** para migraciones de esquema
- **Pytest** para pruebas unitarias
- **Docker** (opcional pero recomendado)
- **MkDocs** para documentación

---

## ✅ Tareas Principales

### 1. Configuración del Proyecto
- Crear entorno virtual y configurar dependencias en `requirements.txt` o `pyproject.toml`.
- Configurar conexión a **PostgreSQL**.
- Definir modelos de datos (`Book`, `Review`) utilizando SQLAlchemy/SQLModel.
- Crear migraciones iniciales con **Alembic**.

### 2. Implementación del CRUD con FastAPI
- **Endpoints para `Book`**:  
  - Crear libro  
  - Listar libros  
  - Obtener un libro por `id`  
  - Actualizar libro  
  - Eliminar libro  
- **Endpoints para `Review`**:  
  - Crear reseña para un libro  
  - Listar reseñas de un libro  
  - Actualizar reseña  
  - Eliminar reseña  

### 3. Pruebas Unitarias y Documentación
- Configurar **pytest** y base de datos de pruebas.
- Escribir pruebas unitarias para:  
  - Creación de libros y reseñas.  
  - Validaciones de campos (`rating < 5`, obligatoriedad de ciertos campos).  
  - Relaciones entre `Book` y `Review`.  
  - Actualización y eliminación de registros.  
- Incluir **fixtures** para inicializar datos de prueba.  
- Crear documentación del proyecto con **MkDocs**:  
  - Instalar MkDocs:  
    ```bash
    pip install mkdocs mkdocs-material
    ```
  - Crear archivo de configuración `mkdocs.yml`.
  - Documentar el diseño del proyecto, modelos de datos, endpoints y ejemplos de uso.
  - Generar documentación localmente:  
    ```bash
    mkdocs serve
    ```
  - Generar documentación estática:  
    ```bash
    mkdocs build
    ```

---

## 🚀 Ejecución del Proyecto

1. Clonar el repositorio.  
2. Instalar dependencias:  
   ```bash
   pip install -r requirements.txt
