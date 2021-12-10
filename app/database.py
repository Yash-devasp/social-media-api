from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:yash1234@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        connection = psycopg2.connect(host="localhost",dbname="fastapi",user="postgres",password="yash1234",cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Connection successful!")
        break
    except Exception:
        print("Connection unsuccessful!")
        time.sleep(30)