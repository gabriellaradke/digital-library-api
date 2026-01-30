from sqlalchemy import select, func
from sqlalchemy.orm import Session
from . import models

# -------- USERS --------
def create_user(db: Session,
                name: str,
                email: str) -> models.User:
    user = models.User(name=name,
                       email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session,
             user_id: int) -> models.User | None:
    return db.get(models.User,
                  user_id)

def get_user_by_email(db: Session,
                      email: str) -> models.User | None:
    stmt = select(models.User).where(models.User.email == email)
    return db.scalar(stmt)

def list_users(db: Session,
               skip: int, limit: int) -> list[models.User]:
    stmt = select(models.User).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def update_user(db: Session,
                user: models.User,
                name: str | None,
                email: str | None) -> models.User:
    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    db.commit()
    db.refresh(user)
    return user

def list_user_loans(db: Session,
                    user_id: int,
                    active_only: bool | None) -> list[models.Loan]:
    stmt = select(models.Loan).where(models.Loan.user_id == user_id)
    if active_only is True:
        stmt = stmt.where(models.Loan.return_date.is_(None))
    if active_only is False:
        stmt = stmt.where(models.Loan.return_date.is_not(None))
    return list(db.scalars(stmt.order_by(models.Loan.loan_date.desc())).all())


# -------- BOOKS --------
def create_book(db: Session,
                title: str,
                author: str,
                total_copies: int) -> models.Book:
    book = models.Book(
        title=title,
        author=author,
        total_copies=total_copies,
        available_copies=total_copies,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_book(db: Session,
             book_id: int) -> models.Book | None:
    return db.get(models.Book,
                  book_id)

def list_books(db: Session,
               skip: int,
               limit: int) -> list[models.Book]:
    stmt = select(models.Book).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def update_book(db: Session,
                book: models.Book,
                title: str | None,
                author: str | None,
                total_copies: int | None) -> models.Book:
    if title is not None:
        book.title = title
    if author is not None:
        book.author = author

    if total_copies is not None:
        used = book.total_copies - book.available_copies
        book.total_copies = total_copies
        book.available_copies = max(total_copies - used, 0)

    db.commit()
    db.refresh(book)
    return book


# -------- LOANS --------
def count_active_loans_for_user(db: Session, 
                                user_id: int) -> int:
    stmt = select(func.count()).select_from(models.Loan).where(
        models.Loan.user_id == user_id,
        models.Loan.return_date.is_(None),
    )
    return int(db.scalar(stmt) or 0)

def create_loan(db: Session,
                user_id: int,
                book_id: int,
                due_date) -> models.Loan:
    loan = models.Loan(user_id=user_id,
                       book_id=book_id,
                       due_date=due_date)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def get_loan(db: Session,
             loan_id: int) -> models.Loan | None:
    return db.get(models.Loan,
                  loan_id)

def list_loans(db: Session,
               skip: int,
               limit: int) -> list[models.Loan]:
    stmt = select(models.Loan).offset(skip).limit(limit).order_by(models.Loan.loan_date.desc())
    return list(db.scalars(stmt).all())
