from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


async def send_email(email: EmailStr, subject: str, body: str):
    message = MessageSchema(
        subject=subject, recipients=[email], body=body, subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)


# ✅ Welcome Email
async def send_welcome_email(email: EmailStr, username: str):

    subject = "Welcome to Expense Tracker"

    body = f"""
    <h2>Hello {username} 👋</h2>
    <p>Your account has been successfully created.</p>
    <p>Start tracking your expenses now!</p>
    <br>
    <p>Thank you for using <b>Expense Tracker</b>.</p>
    """

    await send_email(email, subject, body)


# ✅ Password Reset Email
async def send_password_reset_email(email: EmailStr, reset_link: str):

    subject = "Reset Your Password"

    body = f"""
    <h3>Password Reset Request</h3>
    <p>You requested to reset your password.</p>
    <p>Click the link below to reset it:</p>

    <a href="{reset_link}" 
       style="padding:10px 20px;background:#4CAF50;color:white;text-decoration:none;border-radius:5px;">
       Reset Password
    </a>

    <p>This link will expire in 15 minutes.</p>

    <br>
    <p>If you did not request this, please ignore this email.</p>
    """

    await send_email(email, subject, body)
