from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from contextlib import contextmanager



class Base(DeclarativeBase):
    pass



db = SQLAlchemy(model_class=Base)


session = db.session


@contextmanager
def session_scope(is_commit: bool = True, is_close: bool = True):
    try:
        yield session

        if is_commit:
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        if is_close:
            session.close()
