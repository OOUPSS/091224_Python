from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import db, Question
from schemas.question import QuestionCreate, QuestionResponse
from typing import List

router = APIRouter()

@router.get("/questions", response_model=List[QuestionResponse])
def get_questions(db_session: Session = Depends(get_db)):
    questions = db_session.query(Question).all()
    return questions

@router.post("/questions", response_model=QuestionResponse)
def create_question(question: QuestionCreate, db_session: Session = Depends(get_db)):
    db_question = Question(content=question.content, category_id=question.category_id)
    db_session.add(db_question)
    db_session.commit()
    db_session.refresh(db_question)
    return db_question
