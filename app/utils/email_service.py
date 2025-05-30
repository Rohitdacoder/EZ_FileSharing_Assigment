# app/utils/email_service.py

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("EMAIL_USER")

def send_verification_email(to_email, token):
    verify_url = f"http://localhost:8000/auth/verify?token={token}"

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="Verify your Email",
        html_content=f"""
        <p>Hi there,</p>
        <p>Click below to verify your email:</p>
        <a href="{verify_url}">{verify_url}</a>
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("Email sent:", response.status_code)
    except Exception as e:
        print("Email send failed:", e)
