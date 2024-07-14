from contextlib import contextmanager
from db import db
from sqlalchemy.orm import Session



@contextmanager
def session_scope(session: Session = None, is_commit = True):
    session = db.session() if not session else session
    try:
        yield session

        if is_commit:
            session.commit()
    except Exception:
        session.rollback()
        raise