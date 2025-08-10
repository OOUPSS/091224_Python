from pydantic import BaseModel
from typing import List

class CategoryBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class QuestionCreate(BaseModel):
    content: str
    category_id: int

    class Config:
        orm_mode = True

class QuestionResponse(BaseModel):
    id: int
    content: str
    category: CategoryResponse

    class Config:
        orm_mode = True
