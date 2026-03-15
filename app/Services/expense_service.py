from http.client import HTTPException

from sqlalchemy.orm import Session
from app.models.expense_model import Expense
from app.models.user_model import User
from app.schemas.expense_schema import ExpenseCreate
from sqlalchemy import func, extract


def create_expense(db: Session, expense: ExpenseCreate, username: str):

    user = db.query(User).filter(User.username == username, User.deleted == False).first()

    new_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        user_id=user.id,
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


def get_all_expenses(db: Session, username: str):

    user = db.query(User).filter(User.username == username, User.deleted == False).first()

    return db.query(Expense).filter(Expense.user_id == user.id,Expense.is_active == False).all()


def get_expense_by_id(db: Session, expense_id: int):

    return db.query(Expense).filter(Expense.id == expense_id,Expense.is_active == False).first()


def get_expense_by_category(db: Session, category: str):
    return db.query(Expense).filter(Expense.category == category,Expense.is_active == False).all()


def get_total_expense(db: Session):

    total = db.query(func.sum(Expense.amount)).scalar()

    return total if total else 0


def get_monthly_expense(db: Session, month: int):

    return db.query(Expense).filter(extract("month", Expense.date) == month).all()


def update_expense(db: Session, expense_id: int, expense: ExpenseCreate):

    db_expense = db.query(Expense).filter(Expense.id == expense_id,Expense.is_active == False).first()

    if not db_expense:
        return None

    db_expense.title = expense.title
    db_expense.amount = expense.amount
    db_expense.category = expense.category

    db.commit()
    db.refresh(db_expense)

    return db_expense


def delete_expense(db, expense_id: int, user_id: int):

    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == user_id)
        .first()
    )

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.is_active = True

    db.commit()

    return {"message": "Expense deleted successfully"}
