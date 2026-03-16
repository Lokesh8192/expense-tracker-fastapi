from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.database import get_db
from app.models.expense_model import Expense
from app.schemas.expense_schema import ExpenseCreate
from app.Services.expense_service import (
    create_expense,
    delete_expense,
    get_expense_by_category,
    get_expense_by_id,
    get_monthly_expense,
    get_total_expense,
    update_expense,
)

from app.dependencies.auth_dependency import get_current_user
from app.utils.pagination import paginate
from app.utils.response import success_message, error_message
from app.core.redis import redis_client
import json


router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/")
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    new_expense = create_expense(db, expense, user)

    return success_message("Expense created successfully", new_expense)


@router.get("/")
def get_expenses(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    # `get_current_user` now returns a User model instance
    query = db.query(Expense).filter(Expense.user_id == user.id)

    offset = (page - 1) * page_size
    expenses = query.offset(offset).limit(page_size).all()

    return success_message("Expenses retrieved successfully", expenses)


@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db), user=Depends(get_current_user)):

    total_expense = (
        db.query(func.sum(Expense.amount)).filter(Expense.user_id == user.id).scalar()
    )

    expense_count = db.query(Expense).filter(Expense.user_id == user.id).count()

    top_category = (
        db.query(Expense.category, func.sum(Expense.amount).label("total"))
        .filter(Expense.user_id == user.id)
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
        .first()
    )

    return success_message(
        "Dashboard data fetched successfully",
        {
            "total_expense": total_expense or 0,
            "expense_count": expense_count,
            "top_category": top_category[0] if top_category else None,
        },
    )


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), user=Depends(get_current_user)):

    cache_key = f"dashboard:{user.id}"

    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    total = (
        db.query(func.sum(Expense.amount)).filter(Expense.user_id == user.id).scalar()
    )

    result = {"total_expense": total or 0}

    redis_client.setex(cache_key, 60, json.dumps(result))

    return result


@router.get("/total")
def get_total_expense_api(
    db: Session = Depends(get_db), user=Depends(get_current_user)
):

    total = get_total_expense(db)

    return success_message("Total expense calculated", {"total_expense": total})


@router.get("/{expense_id}")
def get_expense_by_id_api(
    expense_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):

    expense = get_expense_by_id(db, expense_id)

    if not expense:
        return error_message("Expense not found")

    return success_message("Expense retrieved successfully", expense)


@router.put("/{expense_id}")
def update_expense_api(
    expense_id: int,
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    updated = update_expense(db, expense_id, expense)

    if not updated:
        return error_message("Expense not found")

    return success_message("Expense updated successfully", updated)


@router.delete("/{expense_id}")
def delete_expense_api(
    expense_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):

    deleted = delete_expense(db, expense_id)

    if not deleted:
        return error_message("Expense not found")

    return success_message("Expense deleted successfully", {"expense_id": expense_id})


@router.get("/monthly/{month}")
def get_monthly_expense_api(
    month: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):

    expenses = get_monthly_expense(db, month)

    if not expenses:
        return error_message("No expenses found for this month")

    return success_message("Monthly expenses retrieved", expenses)


@router.get("/category/{category}")
def get_expense_by_category_api(
    category: str,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    query = get_expense_by_category(db, category)

    expenses = paginate(query, page, page_size)

    if not expenses:
        return error_message("No expenses found for this category")

    return success_message(f"{category} expenses retrieved", expenses)


import pandas as pd
from fastapi.responses import StreamingResponse
import io


@router.get("/export/csv")
def export_expenses_csv(db: Session = Depends(get_db), user=Depends(get_current_user)):

    expenses = db.query(Expense).filter(Expense.user_id == user.id).all()

    data = [
        {"title": e.title, "amount": e.amount, "category": e.category, "date": e.date}
        for e in expenses
    ]

    df = pd.DataFrame(data)

    stream = io.StringIO()
    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")

    response.headers["Content-Disposition"] = "attachment; filename=expenses.csv"

    return response


@router.get("/export/excel")
def export_excel(db: Session = Depends(get_db), user=Depends(get_current_user)):

    expenses = db.query(Expense).filter(Expense.user_id == user.id).all()

    data = [
        {"title": e.title, "amount": e.amount, "category": e.category, "date": e.date}
        for e in expenses
    ]

    df = pd.DataFrame(data)

    stream = io.BytesIO()

    df.to_excel(stream, index=False)

    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    response.headers["Content-Disposition"] = "attachment; filename=expenses.xlsx"

    return response
