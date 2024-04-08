from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_db = os.getenv('POSTGRES_DB')
database_host = os.getenv('POSTGRES_HOST')

DATABASE_URL = f'postgresql://{postgres_user}:{postgres_password}@{database_host}/{postgres_db}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# FastAPI's dependency injection system allows for cleaner, more modular code.
# It will allow for something like this:
# from fastapi import Depends

# @app.get("/items/")
# def read_items(db: Session = Depends(get_db)):
#     # `db` session can be used here...

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()