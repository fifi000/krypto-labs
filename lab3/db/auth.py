from .models import UserModel
from .config import get_session

from sqlmodel import select


def _session():
    return next(get_session())


def create_user(username: str, password: str) -> None:
    """
    Creates a new user with the given username and password.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.

    Returns:
        None
    """

    user = UserModel(username=username)    
    
    user.set_password(password)    

    # save user to database
    session = _session()    
    session.add(user)
    session.commit()


def is_unique_username(username: str) -> bool:
    """
    Checks if the given username is unique in the database.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the username is unique, False otherwise.
    """
    session = _session()
    
    return not session.exec(
        select(UserModel).where(UserModel.username == username)
    ).first()


def verify_password(username: str, password: str) -> bool:
    """
    Verify the password for a given username.

    Args:
        username (str): The username to verify.
        password (str): The password to verify.

    Returns:
        bool: True if the password is correct for the given username, False otherwise.
    """
    session = _session()
    
    user = session.exec(
        select(UserModel).where(UserModel.username == username)
    ).first()
    
    if not user:
        return False
    
    return user.verify_password(password)