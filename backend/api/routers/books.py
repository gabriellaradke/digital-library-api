from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from ..database import get_db
from .. import schemas, crud
from ..utils import clamp_pagination

logger = logging.getLogger("library.api")

router = APIRouter(prefix="/books",
                   tags=["books"])

# -------- CREATE --------
@router.post("",
             response_model=schemas.BookOut,
             status_code=201)
def create_book(payload: schemas.BookCreate,
                db: Session = Depends(get_db)):
     book = crud.create_book(db,
                             payload.title,
                             payload.author,
                             payload.total_copies)
     logger.info("book_created book_id=%s title=%s",
                 book.id,
                 book.title)
     return book

# -------- LIST --------
@router.get("",
            response_model=list[schemas.BookOut])
def list_books(skip: int = 0,
               limit: int = 20,
               db: Session = Depends(get_db)):
    skip, limit = clamp_pagination(skip, limit)
    return crud.list_books(db,
                           skip,
                           limit)

# -------- GET INFO --------
@router.get("/{book_id}",
            response_model=schemas.BookOut)
def get_book(book_id: int,
             db: Session = Depends(get_db)):
    book = crud.get_book(db,
                         book_id)
    if not book:
        raise HTTPException(status_code=404,
                            detail="Book not found")
    return book

# -------- UPDATE --------
@router.put("/{book_id}",
            response_model=schemas.BookOut)
def update_book(book_id: int,
                payload: schemas.BookUpdate,
                db: Session = Depends(get_db)):
    book = crud.get_book(db,
                         book_id)
    if not book:
        raise HTTPException(status_code=404,
                            detail="Book not found")
    updated = crud.update_book(db,
                               book,
                               payload.title,
                               payload.author,
                               payload.total_copies)
    logger.info("book_updated book_id=%s title=%s",
                updated.id,
                updated.title)
    return updated

# -------- CHECK AVAILABILITY --------
@router.get("/{book_id}/availability")
def availability(book_id: int,
                 db: Session = Depends(get_db)):
    book = crud.get_book(db,
                         book_id)
    if not book:
        raise HTTPException(status_code=404,
                            detail="Book not found")
    return {"book_id": book.id,
            "available_copies": book.available_copies,
            "total_copies": book.total_copies}
