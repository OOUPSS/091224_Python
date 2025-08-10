import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.core.config import Settings
from src.db.database import Base, engine, get_db
from src.api.endpoints import task_router
from src.api.middleware.request_logging import RequestLoggingMiddleware

# Создание экземпляра FastAPI
app = FastAPI(title="Custom API Project")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=RequestLoggingMiddleware())

# Включение маршрутов
app.include_router(task_router.router, prefix="/api/v1")

# Проверка и создание таблиц базы данных
# Этот код будет выполнен при запуске приложения
# В реальном проекте лучше использовать alembic для миграций
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Custom API!"}