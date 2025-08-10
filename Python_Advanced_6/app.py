from fastapi import FastAPI
from routes.category import router as category_router
from routes.question import router as question_router

app = FastAPI()

app.include_router(category_router)
app.include_router(question_router)

from sqlalchemy.orm import Session
from models import db

def get_db():
    db_session = db.session()
    try:
        yield db_session
    finally:
        db_session.close()
