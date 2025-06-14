import os

from dotenv import load_dotenv

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, FastAPIError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import InvalidRequestError
from starlette.exceptions import HTTPException as StarletteHttpException
import uvicorn

from app.utils.database import Base, engine
from app.routers import route

from app.response.error_response import ValidationErrorResponse,ErrorResponse
from app.response.success_response import success_response
from app.model import *
load_dotenv()

# create database tables

Base.metadata.create_all(engine)

app = FastAPI()

# routes
app.include_router(route)

# cors handler, 배포시에는 안전한 cors로 바꾸어야 함

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# validation exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": error.get("loc")[-1],
                "message": error.get("msg"),
            }
        )
    response = ValidationErrorResponse(errors=errors)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response.model_dump()
    )


@app.exception_handler(StarletteHttpException)
async def http_exception_handler(request: Request, exc: StarletteHttpException):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(status_code=exc.status_code, message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())


@app.exception_handler(InvalidRequestError)
async def http_exception_handler(request: Request, exc: InvalidRequestError):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=exc._message()
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.model_dump()
    )

@app.exception_handler(FastAPIError)
async def http_exception_handler(request: Request, exc: FastAPIError):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=exc.detail
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.model_dump()
    )


@app.get("/")
async def index():
    return success_response(message = "welcome to courtvision")


