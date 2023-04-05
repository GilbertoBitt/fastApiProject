import os
from msilib import Table

from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float, PrimaryKeyConstraint, ForeignKey, \
    BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import *

Base = declarative_base()


class User(Base):
    __tablename__ = "User"
    phone = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=False)
    name = Column(String)
    score = Column(BigInteger)


app = FastAPI()

DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')
User.__table__.create(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {DATABASE_URL}"}


@app.get("/hello/{name}/phone/{phone}/score/{score}")
async def say_hello(name: str, phone: str, score: int):
    session = Session()
    user = session.query(User).filter(User.phone == phone).first()
    if user:
        user.name += name
        if user.score < score:
            user.score = score
        session.commit()
    else:
        session.add(User(name=name, phone=phone, score=score))
        session.commit()
    return {"message": f"Hello {name}, your phone number is {phone}"}


@app.get("/topScores")
async def top_scores():
    session = Session()
    users = session.query(User).order_by(User.score.desc()).limit(10).all()
    return users
