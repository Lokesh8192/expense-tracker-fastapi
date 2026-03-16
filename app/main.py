from fastapi import FastAPI
from app.database.database import engine,Base
from app.routers import expense_router,auth_router
from app.models import expense_model
from app.middleware.logging_middleware import LoggingMiddleware

app=FastAPI(
    title="Expense Tracker API",
    description="FastAPI+Postgres Expense Tracker",
    version="1.0"
)

Base.metadata.create_all(bind=engine)


app.add_middleware(LoggingMiddleware)

app.include_router(expense_router.router)
app.include_router(auth_router.router)
