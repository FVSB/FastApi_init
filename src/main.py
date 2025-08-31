from fastapi import FastAPI
from src.books.routes import book_router
from src.tags.routes import tags_router
from src.utils.errors import register_all_errors
version = "v1"

description = """
A REST API for a book review web service.

This REST API is able to;
- Create Read Update And delete books
- Add reviews to books
"""


version_prefix =f"/api/{version}"

app = FastAPI(name="Book Demo",
    version=version,
              description=description)  


register_all_errors(app)

app.include_router(book_router, prefix=f"{version_prefix}/books", tags=["books"])
app.include_router(tags_router, prefix=f"{version_prefix}/tags", tags=["tags"])
