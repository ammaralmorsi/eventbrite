import os

from enum import Enum

from fastapi import HTTPException
from fastapi import status
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from datetime import timedelta

"""
This module contains a class EmailHandler that is used for sending emails using the Gmail SMTP server. The class 
defines two types of emails, SIGNUP_VERIFICATION and FORGET_PASSWORD, and generates the HTML content for both types of 
emails. The class also has a method for sending emails.

Functions:
    - __init__(): Initializes the class with the necessary instance variables.
    - generate_html_for_signup_verification(token: str): Generates the HTML content for SIGNUP_VERIFICATION email.
    - generate_html_for_forgot_password(token: str): Generates the HTML content for FORGET_PASSWORD email.
    - get_email_body(email_type: EmailType, token: str): Returns the HTML content for the specified email type.
    - send_email(email: str, token: str, email_type: EmailType): Sends an email of the specified email type to the 
      specified email address.

Constants:
    - EmailType: An enum that defines the two types of emails, SIGNUP_VERIFICATION and FORGET_PASSWORD.

Usage:
    Create an instance of the EmailHandler class and use the send_email method to send emails. The method takes an 
    email address, a token, and an email type as parameters. The email type determines the content of the email.
"""

class EmailType(Enum):
    SIGNUP_VERIFICATION = "SIGNUP_VERIFICATION"
    FORGET_PASSWORD = "FORGET_PASSWORD"


class EmailHandler:
    def __init__(self):
        self.source_email = os.environ.get("EVENTBRITE_EMAIL")
        self.source_password = os.environ.get("EVENTBRITE_PASSWORD")
        self.message = None
        self.expiration_date = datetime.utcnow() + timedelta(hours=24)
        self.host = os.environ.get("FRONT_HOSTNAME")

    def generate_html_for_signup_verification(self, token):
        verification_link = f"{self.host}/verify?token={token}"
        html = f"<p>Thank you for signing up! Please click the following link to verify your email address:</p>" \
               f"<p><a href='{verification_link}'>{verification_link}</a></p>" \
               f"\<p>The link will expire on {self.expiration_date}.</p>"
        return html

    def generate_html_for_forgot_password(self, token):
        verification_link = f"{self.host}/change-password?token={token}"
        html = f"<p>Click the following link to reset your password:</p>" \
               f"<p><a href='{verification_link}'>{verification_link}</a></p>" \
               f"<p>The link will expire on {self.expiration_date}.</p>"
        return html

    def get_email_body(self, email_type: EmailType, token: str):
        return self.generate_html_for_signup_verification(token) if email_type == EmailType.SIGNUP_VERIFICATION \
            else self.generate_html_for_forgot_password(token)

    def send_email(self, email: str, token: str, email_type: EmailType):
        self.message = MIMEMultipart()
        self.message["From"] = self.source_email
        self.message["To"] = email
        self.message["Subject"] = "Verification email"
        body = self.get_email_body(email_type, token)
        self.message.attach(MIMEText(body, "html"))
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            # server.starttls()
            server.login(self.source_email, self.source_password)
            server.sendmail(self.source_email, email, self.message.as_string())
        except smtplib.SMTPRecipientsRefused:
            raise HTTPException(detail="recipient email refused.",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except smtplib.SMTPException:
            raise HTTPException(detail="failed to send email.",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except AttributeError:
            raise HTTPException(detail="no source email.",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
