import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

# ==============================
# ENV VARIABLES
# ==============================
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")


# ==============================
# SEND EMAIL (SendGrid)
# ==============================
async def send_email(email: str, subject: str, body: str):
    print("\n📧 Sending Email...")

    if not SENDGRID_API_KEY:
        raise RuntimeError("Missing SENDGRID_API_KEY")

    if not EMAIL_FROM:
        raise RuntimeError("Missing EMAIL_FROM")

    try:
        message = Mail(
            from_email=EMAIL_FROM,
            to_emails=email,
            subject=subject,
            html_content=body,
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        print("✅ Email Sent:", response.status_code)

    except Exception as e:
        error_message = str(e)

        try:
            status = getattr(e, "status_code", None)
            body = getattr(e, "body", None)
            if status or body:
                error_message = f"{status} {body}"
        except Exception:
            pass

        print("❌ SendGrid Error:", error_message)
        raise


# ==============================
# EMAIL TEMPLATES
# ==============================


# Welcome Email
async def send_welcome_email(email: str, username: str):
    subject = "Welcome to Expense Tracker"
    body = f"""
    <h2>Hello {username} 👋</h2>
    <p>Your account has been successfully created.</p>
    <p>Start tracking your expenses now!</p>
    """
    await send_email(email, subject, body)


# Password Reset Email
async def send_password_reset_email(email: str, reset_link: str):
    subject = "Reset Your Password"
    body = f"""
    <h3>Password Reset Request</h3>
    <p>Click below to reset your password:</p>
    <a href="{reset_link}">Reset Password</a>
    """
    await send_email(email, subject, body)


# Email Verification
async def send_verification_email(email: str, username: str, verification_link: str):
    subject = "Verify your email address"
    body = f"""
    <h3>Hello {username} 👋</h3>
    <p>Please verify your email:</p>
    <a href="{verification_link}">Verify Email</a>
    """
    await send_email(email, subject, body)
