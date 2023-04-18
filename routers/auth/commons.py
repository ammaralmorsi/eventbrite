from .db.driver import get_db_conn
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jwt
import secrets
from datetime import datetime, timedelta
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret_key = secrets.token_hex(32)

def is_unique(email):
    """
    Check if a given email address is unique and not already in use.

    Parameters:
    email (str): Email address to check

    Returns:
    bool: True if the email is unique, False otherwise
    """
    db = get_db_conn()
    logged_user = db["User"].find_one({"email": email})
    if logged_user is not None:
        return False
    return True

def verify_password(plain_password, hashed_password):
    """
    Verify a given plain-text password against a hashed password.

    Parameters:
    plain_password (str): Plain-text password to verify
    hashed_password (str): Hashed password to verify against

    Returns:
    bool: True if the passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Generate a hash for a given plain-text password.

    Parameters:
    password (str): Plain-text password to hash

    Returns:
    str: Hashed password
    """
    return pwd_context.hash(password)

def encode_token(email):
    """
    Encode a JWT token containing the user's email address and expiration time.

    Parameters:
    email (str): User's email address

    Returns:
    str: Encoded JWT token
    """
    encoded_token = jwt.encode({"email": email, "exp": datetime.utcnow() + timedelta(hours=24)}, secret_key, algorithm="HS256")
    return encoded_token

def decode_token(token):
    """
    Decode a JWT token and extract the user's email address and expiration time.

    Parameters:
    token (str): JWT token to decode

    Returns:
    tuple: Email address and expiration time extracted from the token
    """
    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    email = payload["email"]
    expiration_time = datetime.fromtimestamp(payload["exp"])
    return email, expiration_time


def send_email(email: str, token: str, email_type: int):
    """
    Send a verification email to the specified email address with a verification link containing the given token.

    Parameters:
        email (str): Email address to send the verification email to.
        token (str): JSON Web Token to include in the verification link.
        email_type: integer define whether the email will be signup verification email (1) or forgot password email (2)

    Returns:
        1- code tell whether an error is happened
        2- body describes the behaviour
    """
    source_email = os.environ.get("EVENTBRITE_EMAIL")
    source_password = os.environ.get("EVENTBRITE_PASSWORD")
    message = MIMEMultipart()
    message["From"] = os.environ.get("EMAIL")
    message["To"] = email
    message["Subject"] = "Verification email"
    expiration_date = datetime.utcnow() + timedelta(hours=24)
    if email_type == 1:
        verification_link = f"http://127.0.0.1:8000/auth/verify?token={token}"
        html = f"<p>Thank you for signing up! Please click the following link to verify your email address:</p><p><a href='{verification_link}'>{verification_link}</a></p><p>The link will expire on {expiration_date}.</p>"
    else:
        verification_link = f"http://127.0.0.1:8000/auth/reset-password?token={token}"
        html = f"<p>Click the following link to reset your password:</p><p><a href='{verification_link}'>{verification_link}</a></p><p>The link will expire on {expiration_date}.</p>"
    message.attach(MIMEText(html, "html"))
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        try:
            server.starttls()
            server.login(source_email, source_password)
            server.sendmail(source_email, email, message.as_string())
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

