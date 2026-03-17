from fastapi import FastAPI
from app.database.database import engine, Base
from app.routers import expense_router, auth_router
from app.models import expense_model, user_model
from app.middleware.logging_middleware import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text


app = FastAPI(
    title="Expense Tracker API",
    description="FastAPI+Postgres Expense Tracker",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.35:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _ensure_user_columns():
    inspector = inspect(engine)

    if not inspector.has_table(user_model.User.__tablename__):
        return

    existing_cols = {
        col["name"] for col in inspector.get_columns(user_model.User.__tablename__)
    }

    with engine.connect() as conn:
        if "email_verified" not in existing_cols:
            conn.execute(
                text(
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT false"
                )
            )


# ensure schema is up to date
Base.metadata.create_all(bind=engine)
_ensure_user_columns()


app.add_middleware(LoggingMiddleware)

app.include_router(expense_router.router)
app.include_router(auth_router.router)
