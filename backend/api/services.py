from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from . import crud, models
from .utils import days_overdue

logger = logging.getLogger("library.services")

LOAN_DAYS = 14
FINE_PER_DAY = 2
MAX_ACTIVE_LOANS = 3

# -------- BORROW --------
def borrow_book(db: Session,
                user_id: int,
                book_id: int) -> models.Loan:
    user = crud.get_user(db,
                         user_id)
    if not user:
        raise HTTPException(status_code=404,
                            detail="User not found")

    book = crud.get_book(db,
                         book_id)
    if not book:
        raise HTTPException(status_code=404,
                            detail="Book not found")

    if book.available_copies <= 0:
        raise HTTPException(status_code=409,
                            detail="No available copies")

    active_count = crud.count_active_loans_for_user(db,
                                                    user_id)
    if active_count >= MAX_ACTIVE_LOANS:
        raise HTTPException(status_code=409,
                            detail="User reached max active loans")

    due_date = datetime.now(timezone.utc) + timedelta(days=LOAN_DAYS) 

    book.available_copies -= 1
    loan = crud.create_loan(db,
                            user_id=user_id,
                            book_id=book_id,
                            due_date=due_date)
    
    logger.info(
        "loan_created loan_id=%s user_id=%s book_id=%s due_date=%s",
        loan.id,
        user_id,
        book_id,
        due_date.isoformat()
        )
    
    return loan

# -------- RETURN --------
def return_loan(db: Session,
                loan_id: int) -> models.Loan:
    loan = crud.get_loan(db,
                         loan_id)
    if not loan:
        raise HTTPException(status_code=404,
                            detail="Loan not found")
    if loan.return_date is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Loan already returned")

    book = crud.get_book(db,
                         loan.book_id)
    if not book:
        raise HTTPException(status_code=404,
                            detail="Book not found")

    now = datetime.now(timezone.utc)
    overdue_days = days_overdue(loan.due_date,
                                now)
    loan.return_date = now
    loan.fine_amount = overdue_days * FINE_PER_DAY

    book.available_copies = min(book.available_copies + 1,
                                book.total_copies)

    db.commit()
    db.refresh(loan)
    
    logger.info(
        "loan_returned loan_id=%s user_id=%s book_id=%s fine=%s overdue_days=%s",
        loan.id,
        loan.user_id,
        loan.book_id,
        loan.fine_amount,
        overdue_days
        )

    return loan
