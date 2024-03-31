import hashlib
import os
from typing import Optional

from sqlmodel import SQLModel, Field
from pydantic import validator


class UserModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(min_length=6, max_length=128, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    salt: str = Field(nullable=False)
    
    def set_password(self, password: str):
        if len(password) < 12:
            raise ValueError('Password must be at least 12 characters long')

        # generate a 32-byte salt
        self.salt = os.urandom(32).hex()

        # create a hash combining the password and the salt using sha-256
        hasher = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(self.salt), 100_000)

        self.hashed_password = hasher.hex()

