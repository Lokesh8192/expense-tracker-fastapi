from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.expense_schema import ExpenseCreate
from app.Services.expense_service import (
    create_expense,
    delete_expense,
    get_all_expenses,
    get_expense_by_category,
    get_expense_by_category,
    get_expense_by_id,
    get_expense_by_id,
    get_monthly_expense,
    get_total_expense,
    update_expense,
)
from app.dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/")
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db),user: str = Depends(get_current_user)):
    new_expense = create_expense(db, expense, user)
    return {
        "Status": "Success",
        "message": "Expense Created Successfully",
        "data": new_expense,
    }


@router.get("/")
def get_expense(db: Session = Depends(get_db),user: str = Depends(get_current_user)):
    return get_all_expenses(db,user)


@router.get("/total")
def get_total_expense_api(db: Session = Depends(get_db)):
    total = get_total_expense(db)

    return {"message": "Total expense calculated", "total_expense": total}


@router.get("/{expense_id}")
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = get_expense_by_id(db, expense_id)

    if not expense:
        return {"message": "Expense not found"}

    return expense

@router.get("/monthly/{month}")
def get_monthly_expense_api(month: int, db: Session = Depends(get_db)):
    expenses = get_monthly_expense(db, month)

    if not expenses:
        return {"message": "No expenses found for this month"}

    return expenses

@router.get("/category/{category}")
def get_expense_by_category_api(category: str, db: Session = Depends(get_db)):

    expenses = get_expense_by_category(db, category)

    if not expenses:
        return {"message": "No expenses found for this category"}

    return expenses


@router.put("/{expense_id}")
def update_expense_api(
    expense_id: int, expense: ExpenseCreate, db: Session = Depends(get_db)
):

    updated = update_expense(db, expense_id, expense)

    if not updated:
        return {"message": "Expense not found"}

    return {"message": "Expense updated successfully", "data": updated}


@router.delete("/{expense_id}")
def delete_expense_api(expense_id: int, db: Session = Depends(get_db)):

    deleted = delete_expense(db, expense_id)

    if not deleted:
        return {"message": "Expense not found"}

    return {"message": "Expense deleted successfully", "expense_id": expense_id}
