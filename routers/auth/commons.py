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


def send_verification_email(email: str, token: str):
    """
    Send a verification email to the specified email address with a verification link containing the given token.

    Parameters:
        email (str): Email address to send the verification email to.
        token (str): JSON Web Token to include in the verification link.

    Returns:
        None.
    """
    # Create a message object
    source_email = os.environ.get("EVENTBRITE_EMAIL")
    source_password = os.environ.get("EVENTBRITE_PASSWORD")
    message = MIMEMultipart()
    message["From"] = os.environ.get("EMAIL")
    message["To"] = email
    message["Subject"] = "Verify your email address"
    # Calculate token expiration date (e.g. 1 hour)
    expiration_date = datetime.utcnow() + timedelta(hours=24)
    # Create the verification link with the token
    verification_link = f"http://127.0.0.1:8000/auth/verify?token={token}"
    html = f"<p>Thank you for signing up! Please click the following link to verify your email address:</p><p><a href='{verification_link}'>{verification_link}</a></p><p>The link will expire on {expiration_date}.</p>"
    # Attach the HTML content to the message
    message.attach(MIMEText(html, "html"))
    # Create a connection to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(source_email, source_password)
        server.sendmail(source_email, email, message.as_string())


def send_forgot_password_email(email, token):
    """
    Sends an email to the specified email address containing a link to reset the user's password.

    Args:
        email (str): The email address of the user.
        token (str): The token generated for the password reset request.

    Raises:
        smtplib.SMTPException: If the SMTP server encounters an error.

    Returns:
        None.
    """
    source_email = os.environ.get("EVENTBRITE_EMAIL")
    source_password = os.environ.get("EVENTBRITE_PASSWORD")
    message = MIMEMultipart()
    message["From"] = os.environ.get("EMAIL")
    message["To"] = email
    message["Subject"] = "Reset your password"
    expiration_date = datetime.utcnow() + timedelta(hours=24)
    verification_link = f"http://127.0.0.1:8000/auth/reset-password?token={token}"
    html = f"<p>Click the following link to reset your password:</p><p><a href='{verification_link}'>{verification_link}</a></p><p>The link will expire on {expiration_date}.</p>"
    message.attach(MIMEText(html, "html"))
    # Create a connection to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(source_email, source_password)
        # Send the message
        server.sendmail(source_email, email, message.as_string())

