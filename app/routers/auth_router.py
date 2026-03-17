import os

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

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
    update_user,
)
from app.models.user_model import User
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.email_service import (
    send_email,
    send_welcome_email,
    send_password_reset_email,
    send_verification_email,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------
@router.post("/register", response_model=UserRegisterResponse)
async def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    new_user = create_user(db, user)

    # -----------------------------------
    # EMAIL VERIFICATION (MANDATORY)
    # -----------------------------------
    base_url = os.getenv("BASE_URL", "http://localhost:8000")

    verification_token = jwt.encode(
        {
            "sub": new_user.email,
            "exp": datetime.utcnow() + timedelta(hours=24),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    verification_link = f"{base_url}/auth/verify-email?token={verification_token}"

    background_tasks.add_task(
        send_verification_email,
        new_user.email,
        new_user.username,
        verification_link,
    )

    # -----------------------------------
    # RESPONSE
    # -----------------------------------
    return {
        "success": True,
        "message": ("User registered successfully. " "Please verify your email."),
        "data": new_user,
    }


# ---------------------------------------------------------
# EMAIL VERIFICATION
# ---------------------------------------------------------
@router.get("/verify-email")
def verify_email(
    token: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Verification token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid verification token")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email_verified = True
    db.commit()
    db.refresh(user)

    # Send welcome email once verified
    background_tasks.add_task(send_welcome_email, user.email, user.username)

    return {"status": "Success", "message": "Email verified successfully"}


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
@router.post("/login", response_model=LoginResponse)
async def login(
    user: UserLogin,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):

    db_user = authenticate_user(db, user.username_or_email, user.password)

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token = jwt.encode(
        {"sub": db_user.username, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    # send login alert email
    background_tasks.add_task(
        send_email,
        db_user.email,
        "New Login Alert",
        f"""
        <h3>Hello {db_user.username}</h3>
        <p>You have successfully logged in.</p>
        <p>If this wasn't you, please reset your password immediately.</p>
        """,
    )

    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": token,
            "token_type": "bearer",
            "user": db_user,
        },
    }


# ---------------------------------------------------------
# FORGOT PASSWORD
# ---------------------------------------------------------
@router.post("/forgot-password")
async def forgot_password(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expire = datetime.utcnow() + timedelta(minutes=15)

    reset_token = jwt.encode(
        {"sub": user.email, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    reset_link = f"https://expense-tracker-fastapi-3.onrender.com/reset-password?token={reset_token}"

    background_tasks.add_task(send_password_reset_email, user.email, reset_link)

    return {"status": "Success", "message": "Password reset email sent"}


# ---------------------------------------------------------
# RESET PASSWORD
# ---------------------------------------------------------
@router.post("/reset-password")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db),
):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Reset token expired")

    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = pwd_context.hash(new_password)

    db.commit()

    return {"status": "Success", "message": "Password reset successfully"}


# ---------------------------------------------------------
# GET ALL USERS
# ---------------------------------------------------------
@router.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).filter(User.deleted == False).all()

    return {
        "status": "Success",
        "message": "Users fetched successfully",
        "data": users,
    }


# ---------------------------------------------------------
# GET USER BY ID
# ---------------------------------------------------------
@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id, User.deleted == False).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "status": "Success",
        "message": "User fetched successfully",
        "data": user,
    }


# ---------------------------------------------------------
# UPDATE USER
# ---------------------------------------------------------
@router.put("/{user_id}")
def update_user_api(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
):

    return {
        "Status": "Success",
        "message": "User Updated Successfully",
        "data": update_user(db, user_id, user),
    }


# ---------------------------------------------------------
# DEACTIVATE USER
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# ACTIVATE USER
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# SOFT DELETE USER
# ---------------------------------------------------------
@router.delete("/users/{user_id}")
def soft_delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.deleted = True
    user.is_active = False
    db.commit()

    return {"status": "Success", "message": "User soft deleted successfully"}
