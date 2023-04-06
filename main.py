import os
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
    phone = Column(BigInteger, primary_key=True, unique=True, nullable=False, autoincrement=False)
    name = Column(String)
    score = Column(BigInteger)


app = FastAPI()

DATABASE_URL = os.environ['DATABASE_URL'].replace("postgres://", "postgresql+psycopg2://", 1)
engine = create_engine(DATABASE_URL)
User.__table__.create(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/hello/{name}/phone/{phone}/score/{score}")
async def say_hello(name: str, phone_str: str, score_str: str):
    phone = int(phone_str)
    score = int(score_str)
    session = Session()
    user = session.query(User).filter(User.phone == phone).first()
    if user:
        user.name += name
        if user.score < score:
            user.score = score
        session.commit()
    else:
        user = User(name=name, phone=phone, score=score)
        session.add(user)
        session.commit()
    return user


@app.get("/topScores")
async def top_scores():
    session = Session()
    users = session.query(User).order_by(User.score.desc()).limit(10).all()
    return users
