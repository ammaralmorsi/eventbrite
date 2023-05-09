from passlib.context import CryptContext

"""
This module contains a PasswordHandler class that uses the passlib library to handle password encryption and 
verification. The class has two methods: verify_password and get_password_hash.

Functions:
    - __init__(): Initializes the class with the necessary instance variables.
    - verify_password(plain_password: str, hashed_password: str) -> bool: Verifies the provided plain password 
      against a hashed password, returns True if the verification succeeds, False otherwise.
    - get_password_hash(password: str) -> str: Hashes the provided password and returns the resulting hash string.

Usage:
    Create an instance of the PasswordHandler class and use the verify_password and get_password_hash methods to 
    handle password encryption and verification. The verify_password method takes a plain password and a hashed 
    password as parameters and returns a Boolean value indicating whether the passwords match. The get_password_hash 
    method takes a plain password as a parameter and returns a hash string that can be stored in a database or used 
    for password comparison.
"""

class PasswordHandler:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
