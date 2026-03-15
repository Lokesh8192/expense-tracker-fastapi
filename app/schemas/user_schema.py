from pydantic import BaseModel, EmailStr, field_validator
import re
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone:str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters long")

        if len(value) > 20:
            raise ValueError("Username must be less than 20 characters")

        if not value.isalnum():
            raise ValueError("Username must contain only letters and numbers")

        return value
    
    #email mustend with @gmail.com 
    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not value.strip():
            raise ValueError("Email cannot be empty")
        if not value.endswith("@gmail.com"):
            raise ValueError("Email must be a Gmail address")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if not re.fullmatch(r"[6-9]\d{9}", v):
            raise ValueError("Phone must be a valid 10-digit Indian number")
        return v


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one number")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")

        return value


class UserLogin(BaseModel):
    username_or_email: str
    password: str

    @field_validator("username_or_email")
    @classmethod
    def validate_username_or_email(cls, value):

        if not value.strip():
            raise ValueError("Username or Email cannot be empty")

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if not value.strip():
            raise ValueError("Password cannot be empty")

        return value


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserRegisterResponse(BaseModel):
    success: bool
    message: str
    data: UserResponse


class LoginData(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class LoginResponse(BaseModel):
    success: bool
    message: str
    data: LoginData


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
