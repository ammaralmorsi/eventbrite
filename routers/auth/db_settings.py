from pymongo import MongoClient
from pydantic import BaseModel
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SECRET_KEY = "785c70b3a4426c5bf3b623a6a7011fc4ef04a602f35c0f57852814fe988af8b3"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str

def get_db_conn():
    client = MongoClient('mongodb://localhost:27017')
    db = client['EventBrite']
    return db

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


def send_verification_email(email: str, verification_link: str):
    # Create a message object
    message = MIMEMultipart()
    message["From"] = "a7medmaher309@gmail.com"
    message["To"] = email
    message["Subject"] = "Verify your email address"

    # Create the HTML content of the email
    html = f"<p>Thank you for signing up! Please click the following link to verify your email address:</p><p><a href='{verification_link}'>{verification_link}</a></p>"

    # Attach the HTML content to the message
    message.attach(MIMEText(html, "html"))

    # Create a connection to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("a7medmaher309@gmail.com", "gsrbcwieakzdxyvk")

        # Send the message
        server.sendmail("your_email@example.com", email, message.as_string())
def send_verification(user: User):
    verification_link = f"https://example.com/verify?email={user.email}"
    send_verification_email(user.email, verification_link)

