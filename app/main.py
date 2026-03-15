from fastapi import FastAPI
from app.database.database import engine,Base
from app.routers import expense_router,auth_router
from app.models import expense_model


app=FastAPI(
    title="Expense Tracker API",
    description="FastAPI+Postgres Expense Tracker",
    version="1.0"
)

app.include_router(expense_router.router)
app.include_router(auth_router.router)
