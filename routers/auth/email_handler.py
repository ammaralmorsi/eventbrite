import os

from enum import Enum

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from datetime import timedelta
import socket


class EmailType(Enum):
    SIGNUP_VERIFICATION = "SIGNUP_VERIFICATION"
    FORGET_PASSWORD = "FORGET_PASSWORD"


class EmailHandler:
    def __init__(self):
        self.source_email = os.environ.get("EVENTBRITE_EMAIL")
        self.source_password = os.environ.get("EVENTBRITE_PASSWORD")
        self.message = MIMEMultipart()
        self.message["From"] = os.environ.get("EMAIL")
        self.message["Subject"] = "Verification email"
        self.expiration_date = datetime.utcnow() + timedelta(hours=24)

    def generate_html_for_signup_verification(self, token):
        verification_link = f"http://127.0.0.1:8000/auth/verify?token={token}"
        html = f"<p>Thank you for signing up! Please click the following link to verify your email address:</p>" \
               f"<p><a href='{verification_link}'>{verification_link}</a></p>" \
               f"\<p>The link will expire on {self.expiration_date}.</p>"
        return html

    def generate_html_for_forgot_password(self, token):
        verification_link = f"http://127.0.0.1:8000/auth/reset-password?token={token}"
        html = f"<p>Click the following link to reset your password:</p>" \
               f"<p><a href='{verification_link}'>{verification_link}</a></p>" \
               f"<p>The link will expire on {self.expiration_date}.</p>"
        return html

    def get_email_body(self, email_type: EmailType, token: str):
        return self.generate_html_for_signup_verification(token) if email_type == EmailType.SIGNUP_VERIFICATION \
            else self.generate_html_for_forgot_password(token)

    def send_email(self, email: str, token: str, email_type: EmailType):
        self.message["To"] = email
        body = self.get_email_body(email_type, token)
        self.message.attach(MIMEText(body, "html"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            try:
                server.starttls()
                server.login(self.source_email, self.source_password)
                server.sendmail(self.source_email, email, self.message.as_string())
            except smtplib.SMTPRecipientsRefused as e:
                body = "Recipient email address is invalid."
                return -1, body
            except smtplib.SMTPAuthenticationError as e:
                body = "SMTP authentication error."
                return -1, body
            except Exception as e:
                body = "An error occurred while sending the email."
                return -1, body
            else:
                body = "Successful Request"
                return 1, body
