from sqlalchemy import Boolean, Column, Integer, String
from app.database.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    phone = Column(String, unique=True, nullable=False)
    password = Column(String)

    # Email verification
    email_verified = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)

    # relationship with expenses
    expenses = relationship("Expense", back_populates="user", cascade="all, delete")
