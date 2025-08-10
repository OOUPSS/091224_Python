from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import db, Category
from schemas.question import CategoryBase
from typing import List

router = APIRouter()

@router.post("/categories", response_model=CategoryBase)
def create_category(category: CategoryBase, db_session: Session = Depends(get_db)):
    db_category = Category(name=category.name)
    db.session.add(db_category)
    db.session.commit()
    db.session.refresh(db_category)
    return db_category

@router.get("/categories", response_model=List[CategoryBase])
def get_categories(db_session: Session = Depends(get_db)):
    categories = db_session.query(Category).all()
    return categories

@router.put("/categories/{id}", response_model=CategoryBase)
def update_category(id: int, category: CategoryBase, db_session: Session = Depends(get_db)):
    db_category = db_session.query(Category).filter(Category.id == id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_category.name = category.name
    db_session.commit()
    db_session.refresh(db_category)
    return db_category

@router.delete("/categories/{id}")
def delete_category(id: int, db_session: Session = Depends(get_db)):
    db_category = db_session.query(Category).filter(Category.id == id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_session.delete(db_category)
    db_session.commit()
    return {"message": "Category deleted successfully"}
