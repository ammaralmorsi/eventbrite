from pydantic import BaseModel

class User(BaseModel):
    """
    Represents a user.

    Attributes:
    -----------
    firstname : str
        The user's first name.
    lastname : str
        The user's last name.
    email : str
        The user's email address.
    password : str
        The user's password.
    is_verified : bool, optional
        Whether the user's email address has been verified. Defaults to False.
    """
    firstname: str
    lastname: str
    email: str
    password: str
    is_verified: bool = False

class LoginUser(BaseModel):
    """
    Represents a user attempting to log in.

    Attributes:
    -----------
    email : str
        The user's email address.
    password : str
        The user's password.
    """
    email: str
    password: str



class ChangePasswordRequest(BaseModel):
    """
    Represents a request to change a user's password.

    Attributes:
    -----------
    new_password : str
        The user's new password.
    """
    new_password: str
