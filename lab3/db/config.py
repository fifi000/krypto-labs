try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

import os

from sqlmodel import SQLModel, Session, create_engine


conn = os.getenv('CONNECTION_STRING')
if not conn:
    raise Exception('`CONNECTION_STRING` environment variable is not set')

_engine = create_engine(conn)
SQLModel.metadata.create_all(_engine)


def get_session():
    with Session(_engine) as session:
        yield session


