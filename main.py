import os

from dotenv import load_dotenv

from fastapi import FastAPI

import uvicorn

from app.utils.database import Base, engine
from app.routers import route

from app.response.error_response import ValidationErrorResponse,ErrorResponse
from app.response.success_response import success_response

load_dotenv()

# create database tables

Base.metadata.create(bind=engine)

app = FastAPI()

# routes
app.include_router(route)

@app.get("/")
async def index():
    return success_response(message = "welcome to courtvision")

