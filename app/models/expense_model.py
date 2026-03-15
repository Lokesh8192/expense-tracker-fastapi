from sqlalchemy import Column, DateTime, Integer, String, Float,Date,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import date, datetime


class Expense(Base):

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date=Column(Date, default=date.today)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    is_active = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # relationship with user
    user = relationship("User", back_populates="expenses")
