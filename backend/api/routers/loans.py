from datetime import datetime, timezone
import csv
from io import StringIO
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, crud
from ..services import borrow_book, return_loan
from ..utils import clamp_pagination

router = APIRouter(prefix="/loans",
                   tags=["loans"])

# -------- BORROW --------
@router.post("",
             response_model=schemas.LoanOut,
             status_code=201)
def create_loan(payload: schemas.LoanCreate,
                db: Session = Depends(get_db)):
    return borrow_book(db,
                       payload.user_id,
                       payload.book_id)

# -------- RETURN --------
@router.post("/{loan_id}/return",
             response_model=schemas.LoanOut)
def do_return(loan_id: int,
              db: Session = Depends(get_db)):
    return return_loan(db,
                       loan_id)

# -------- LIST --------
@router.get("",
            response_model=list[schemas.LoanOut])
def list_loans(status: str = "all",
               skip: int = 0,
               limit: int = 20,
               db: Session = Depends(get_db)):
    skip, limit = clamp_pagination(skip, limit)
    loans = crud.list_loans(db,
                            skip,
                            limit)

    if status == "all":
        return loans

    now = datetime.now(timezone.utc)
    if status == "active":
        return [l for l in loans if l.return_date is None]
    if status == "overdue":
        return [l for l in loans if l.return_date is None and l.due_date < now]

    return loans

# -------- EXPORT --------
@router.get("/export/csv")
def export_loans_csv(db: Session = Depends(get_db)):
    loans = crud.list_loans(db,
                            skip=0,
                            limit=1000)

    buffer = StringIO()
    writer = csv.writer(buffer)

    writer.writerow([
        "loan_id",
        "user_id",
        "book_id",
        "loan_date",
        "due_date",
        "return_date",
        "fine_amount",
    ])

    for loan in loans:
        writer.writerow([
            loan.id,
            loan.user_id,
            loan.book_id,
            loan.loan_date.isoformat(),
            loan.due_date.isoformat(),
            loan.return_date.isoformat() if loan.return_date else "",
            loan.fine_amount,
        ])

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=loans.csv"},
    )

