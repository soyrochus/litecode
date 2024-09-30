# LiteCode is a lightweight Python stack for accelerated development of applications and services
#
# Though Litecode, "Single" is the new "Full" stack. Using FastAPI and NiceGUI to build
# web applications entirely on the server side, Litecode removes the need for client-side
# JavaScript or TypeScript, while complexity is reduced by using a simplified architecture
# and single language for the entire stack.
#
# License: MIT License
# For the full license text, please refer to the LICENSE file in the root of the project.
#
# Copyright (c) 2024 Iwan van der Kleijn

from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Create database tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def dbsession(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if _session is already passed; if not, inject a new session
        if '_session' not in kwargs or kwargs['_session'] is None:
            session: Session = SessionLocal()
            kwargs['_session'] = session
            try:
                return func(*args, **kwargs)
            finally:
                session.close()
        else:
            # If _session is already present, just call the function
            return func(*args, **kwargs)
    
    return wrapper