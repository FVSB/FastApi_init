from fastapi import FastAPI
from src.books.routes import router  

version = "v0"

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

app.include_router(router)  