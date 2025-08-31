from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


class BookDemoException(Exception):
    """This is the base class for all book_demo errors"""

    pass



class BookNotFound(BookDemoException):
    """Book Not found"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: BookDemoException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler



def register_all_errors(app: FastAPI):

    app.add_exception_handler(
            BookNotFound,
            create_exception_handler(
                status_code=status.HTTP_404_NOT_FOUND,
                initial_detail={
                    "message": "Book Not Found",
                    "error_code": "book_not_found",
                },
            ),
        )
    
    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
    
    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )