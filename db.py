from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash

engine = create_engine('sqlite:///db.db')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)


def add_user(username, password):
    from models import User

    if get_users().filter_by(username=username).first() is not None:
        return False

    new_user = User(username=username, password=generate_password_hash(password))
    db_session.add(new_user)
    db_session.commit()
    return True


def get_users():
    from models import User

    return db_session.query(User)
