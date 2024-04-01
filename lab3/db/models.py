import os
import hashlib
from typing import Optional

from sqlmodel import SQLModel, Field


import hashlib

def get_hasher(password: str, salt: str):
    """
    Returns the hashed password using PBKDF2 algorithm.

    Parameters:
    - password (str): The password to be hashed.
    - salt (str): The salt used for hashing.

    Returns:
    - bytes: The hashed password.
    """
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100_000)


class UserModel(SQLModel, table=True):
    """
    Represents a user in the system.

    Attributes:
        id (Optional[int]): The user's ID.
        username (str): The user's username.
        hashed_password (str): The hashed password of the user.
        salt (str): The salt used for password hashing.

    Methods:
        set_password(password: str): Sets the user's password.
        verify_password(password: str) -> bool: Verifies if the provided password matches the user's password.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(min_length=6, max_length=128, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    salt: str = Field(nullable=False)
    
    def set_password(self, password: str):
        """
        Sets the password for the user.

        Args:
            password (str): The password to set.

        Raises:
            ValueError: If the password is less than 12 characters long.

        Returns:
            None
        """
        if len(password) < 12:
            raise ValueError('Password must be at least 12 characters long')

        # generate a 32-byte salt
        self.salt = os.urandom(32).hex()

        # create a hash combining the password and the salt using sha-256
        hasher = get_hasher(password, self.salt)

        self.hashed_password = hasher.hex()

    def verify_password(self, password: str) -> bool:
        """
        Verifies if the provided password matches the hashed password stored in the model.

        Args:
            password (str): The password to be verified.

        Returns:
            bool: True if the password matches the hashed password, False otherwise.
        """
        hasher = get_hasher(password, self.salt)
        return hasher.hex() == self.hashed_password


