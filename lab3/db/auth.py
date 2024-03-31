from .models import UserModel
from .config import get_session

from sqlmodel import Session, select


def _session():
    return next(get_session())


def create_user(username: str, password: str):
    user = UserModel(username=username)    
    
    user.set_password(password)    

    # save user to database
    session = _session()    
    session.add(user)
    session.commit()


def is_unique_username(username: str) -> bool:
    session = _session()
    
    return not session.exec(
        select(UserModel).where(UserModel.username == username)
    ).first()