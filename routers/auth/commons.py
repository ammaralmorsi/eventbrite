from .db.driver import get_db_conn
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jwt
import secrets
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret_key = secrets.token_hex(32)

def is_unique(email):
    db = get_db_conn()
    logged_user = db["User"].find_one({"email": email})
    if logged_user is not None:
        return False
    return True

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def encode_token(email):
    encoded_token = jwt.encode({"email": email, "exp": datetime.utcnow() + timedelta(hours=24)}, secret_key, algorithm="HS256")
    return encoded_token

def decode_token(token):
    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    email = payload["email"]
    expiration_time = datetime.fromtimestamp(payload["exp"])
    return email, expiration_time


def send_verification_email(email: str, token: str):
    # Create a message object
    message = MIMEMultipart()
    message["From"] = "a7medmaher309@gmail.com"
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
        server.login("a7medmaher309@gmail.com", "gsrbcwieakzdxyvk")
        server.sendmail("your_email@example.com", email, message.as_string())


def send_forgot_password_email(email, token):
    message = MIMEMultipart()
    message["From"] = "a7medmaher309@gmail.com"
    message["To"] = email
    message["Subject"] = "Verify your email address"
    expiration_date = datetime.utcnow() + timedelta(hours=24)
    verification_link = f"https://example.com/verify?token={token}"
    html = f"<p>Click the following link to reset your password:</p><p><a href='{verification_link}'>{verification_link}</a></p><p>The link will expire on {expiration_date}.</p>"
    message.attach(MIMEText(html, "html"))
    # Create a connection to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("a7medmaher309@gmail.com", "gsrbcwieakzdxyvk")
        # Send the message
        server.sendmail("your_email@example.com", email, message.as_string())

