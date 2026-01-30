from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

# -------- USER --------
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True)
    
    name: Mapped[str] = mapped_column(String(120),
                                      nullable=False)
    
    email: Mapped[str] = mapped_column(String(200),
                                       unique=True,
                                       index=True,
                                       nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=datetime.now(timezone.utc),
                                                 nullable=False)

    loans: Mapped[list["Loan"]] = relationship(back_populates="user")

# -------- BOOK --------
class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True)
    
    title: Mapped[str] = mapped_column(String(200),
                                       nullable=False)
    
    author: Mapped[str] = mapped_column(String(200),
                                        nullable=False)

    total_copies: Mapped[int] = mapped_column(Integer,
                                              default=1,
                                              nullable=False)
    
    available_copies: Mapped[int] = mapped_column(Integer,
                                                  default=1,
                                                  nullable=False)

    loans: Mapped[list["Loan"]] = relationship(back_populates="book")

# -------- LOAN --------
class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                         index=True,
                                         nullable=False)
    
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"),
                                         index=True,
                                         nullable=False)

    loan_date: Mapped[datetime] = mapped_column(DateTime,
                                                default=datetime.now(timezone.utc),
                                                nullable=False)
    
    due_date: Mapped[datetime] = mapped_column(DateTime,
                                               nullable=False)

    return_date: Mapped[datetime | None] = mapped_column(DateTime,
                                                         nullable=True)
    
    fine_amount: Mapped[int] = mapped_column(Integer,
                                             default=0,
                                             nullable=False)

    user: Mapped["User"] = relationship(back_populates="loans")

    book: Mapped["Book"] = relationship(back_populates="loans")
