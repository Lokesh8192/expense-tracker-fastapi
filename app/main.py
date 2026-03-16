from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.database.database import engine,Base
from app.routers import expense_router,auth_router
from app.models import expense_model, user_model
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


@app.get("/reset-password", response_class=HTMLResponse)
def reset_password_page(token: str):
    return f"""
    <html>
        <body>
            <h2>Reset Password</h2>
            <form action="/auth/reset-password" method="post">
                <input type="hidden" name="token" value="{token}" />
                <input type="password" name="new_password" placeholder="Enter new password" required/>
                <button type="submit">Reset Password</button>
            </form>
        </body>
    </html>
    """
