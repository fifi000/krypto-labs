try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

import os
from typing import Any, Generator

from sqlmodel import SQLModel, Session, create_engine


conn = os.getenv('CONNECTION_STRING')
if not conn:
    raise Exception('`CONNECTION_STRING` environment variable is not set')

_engine = create_engine(conn)
SQLModel.metadata.create_all(_engine)


from typing import Generator, Any
from sqlalchemy.orm import Session

def get_session() -> Generator[Session, Any, None]:
    """
    Returns a generator that yields a SQLAlchemy session.

    Yields:
        Session: A SQLAlchemy session object.

    """
    with Session(_engine) as session:
        yield session


