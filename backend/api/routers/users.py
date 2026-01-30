from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from ..database import get_db
from .. import schemas, crud
from ..utils import clamp_pagination

logger = logging.getLogger("library.api")

router = APIRouter(prefix="/users",
                   tags=["users"])

# -------- CREATE --------
@router.post("",
             response_model=schemas.UserOut,
             status_code=201)
def create_user(payload: schemas.UserCreate,
                db: Session = Depends(get_db)):
    if crud.get_user_by_email(db,
                              payload.email):
        raise HTTPException(status_code=409,
                            detail="Email already exists")
    user = crud.create_user(db,
                            name=payload.name,
                            email=str(payload.email))
    logger.info("user_created user_id=%s user_name=%s email=%s",
                user.id,
                user.name,
                user.email)
    return user

# -------- LIST --------
@router.get("",
            response_model=list[schemas.UserOut])
def list_users(skip: int = 0,
               limit: int = 20,
               db: Session = Depends(get_db)):
    skip, limit = clamp_pagination(skip,
                                   limit)
    return crud.list_users(db,
                           skip,
                           limit)

# -------- GET INFO --------
@router.get("/{user_id}",
            response_model=schemas.UserOut)
def get_user(user_id: int,
             db: Session = Depends(get_db)):
    user = crud.get_user(db,
                         user_id)
    if not user:
        raise HTTPException(status_code=404,
                            detail="User not found")
    return user

# -------- UPDATE --------
@router.put("/{user_id}",
            response_model=schemas.UserOut)
def update_user(user_id: int,
                payload: schemas.UserUpdate,
                db: Session = Depends(get_db)):
    user = crud.get_user(db,
                         user_id)
    if not user:
        raise HTTPException(status_code=404,
                            detail="User not found")
    if payload.email and crud.get_user_by_email(db, str(payload.email)) and user.email != str(payload.email):
        raise HTTPException(status_code=409,
                            detail="Email already exists")
    user = crud.update_user(db,
                            user,
                            payload.name,
                            str(payload.email) if payload.email else None)
    logger.info("user_updated user_id=%s user_name=%s email=%s",
                user.id,
                user.name,
                user.email)
    return user

# -------- LIST USER LOANS --------
@router.get("/{user_id}/loans",
            response_model=list[schemas.LoanOut])
def user_loans(user_id: int,
               active_only: bool | None = None,
               db: Session = Depends(get_db)):
    if not crud.get_user(db,
                         user_id):
        raise HTTPException(status_code=404,
                            detail="User not found")
    return crud.list_user_loans(db,
                                user_id=user_id,
                                active_only=active_only)
