import re

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.security import hash_password, verify_password


def _normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone or "")
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    return digits


def create_user(db: Session, user: UserCreate):
    normalized_phone = _normalize_phone(user.phone)

    existing_user = (
        db.query(User)
        .filter(
            or_(
                User.username == user.username,
                User.email == user.email,
                User.phone == normalized_phone,
            )
        )
        .first()
    )

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # want proper message after user registered successfully
    new_user = User(
        username=user.username,
        email=user.email,
        phone=normalized_phone,
        password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, username_or_email: str, password: str):

    user = (
        db.query(User)
        .filter(
            or_(User.username == username_or_email, User.email == username_or_email),
            User.deleted == False,
        )
        .first()
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # check soft delete
    if user.deleted:
        raise HTTPException(status_code=403, detail="User account deleted")

    # check active status
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account deactivated")

    # check email verification
    if not getattr(user, "email_verified", False):
        raise HTTPException(status_code=403, detail="Email not verified")

    return user


def get_all_users(db):
    return db.query(User).filter(User.deleted == False).all()


def get_user_by_id(db, user_id: int):
    user = db.query(User).filter(User.id == user_id, User.deleted == False).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def update_user(db, user_id: int, user_data):

    user = db.query(User).filter(User.id == user_id, User.deleted == False).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(db, user_id: int):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.deleted = True
    db.commit()

    return {"message": "User soft deleted successfully"}
