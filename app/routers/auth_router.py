from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta

from app.database.database import get_db
from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserRegisterResponse,
    LoginResponse,
    UserUpdate,
)
from app.Services.user_service import (
    authenticate_user,
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
)
from app.models.user_model import User
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRegisterResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return {
        "success": True,
        "message": "User registered successfully",
        "data": new_user,
    }


@router.post("/login", response_model=LoginResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = authenticate_user(db, user.username_or_email, user.password)

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token = jwt.encode(
        {"sub": db_user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM
    )

    return {
        "success": True,
        "message": "Login successful",
        "data": {"access_token": token, "token_type": "bearer", "user": db_user},
    }


@router.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).filter(User.deleted == False).all()

    return {"status": "Success", "message": "Users fetched successfully", "data": users}


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id, User.deleted == False).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"status": "Success", "message": "User fetched successfully", "data": user}


@router.put("/{user_id}")
def update_user_api(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return {
        "Status": "Success",
        "message": "User Updated Successfully",
        "data": update_user(db, user_id, user),
    }


@router.patch("/users/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.commit()

    return {
        "status": "Success",
        "message": "User deactivated successfully",
        "data": {"user_id": user.id, "is_active": user.is_active},
    }


@router.patch("/users/{user_id}/activate")
def activate_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()

    return {
        "status": "Success",
        "message": "User activated successfully",
        "data": {"user_id": user.id, "is_active": user.is_active},
    }


@router.delete("/users/{user_id}")
def soft_delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.deleted = True
    user.is_active = False
    db.commit()

    return {"status": "Success", "message": "User soft deleted successfully"}
