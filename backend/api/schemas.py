from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# -------- USERS --------
class UserCreate(BaseModel):
    name: str = Field(min_length=1,
                      max_length=120)
    email: EmailStr

class UserUpdate(BaseModel):
    name: str | None = Field(default=None,
                             min_length=1,
                             max_length=120)
    email: EmailStr | None = None

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# -------- BOOKS --------
class BookCreate(BaseModel):
    title: str = Field(min_length=1,
                       max_length=200)
    author: str = Field(min_length=1,
                        max_length=200)
    total_copies: int = Field(default=1,
                              ge=0)

class BookUpdate(BaseModel):
    title: str | None = Field(default=None,
                              min_length=1,
                              max_length=200)
    author: str | None = Field(default=None,
                               min_length=1,
                               max_length=200)
    total_copies: int | None = Field(default=None,
                                     ge=0)

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    total_copies: int
    available_copies: int

    model_config = {"from_attributes": True}


# -------- LOANS --------
class LoanCreate(BaseModel):
    user_id: int
    book_id: int

class LoanOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    loan_date: datetime
    due_date: datetime
    return_date: datetime | None
    fine_amount: int

    model_config = {"from_attributes": True}
