import asyncio
from datetime import datetime, timedelta
from operator import index

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DATE, ForeignKey, DateTime, column



engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True)
    nick_name = Column(String(100), nullable=False)
    avatar = Column(String(100), nullable=True)
    referal_id = Column(Integer, nullable=True)
    wallet_adress = Column(String(100), nullable=True)
    amount_CRT = Column(Integer, nullable=True, default=0)
    total_balance = Column(Integer, nullable=True, default=0)
    last_watering_ferm1 = Column(DateTime, default=datetime.now() - timedelta(days=2))
    last_watering_ferm2 = Column(DateTime, default=datetime.now() - timedelta(days=2))
    last_watering_ferm3 = Column(DateTime, default=datetime.now() - timedelta(days=2))
    watering_ferm1 = Column(Integer, default=0)
    watering_ferm2 = Column(Integer,default=0)
    watering_ferm3 = Column(Integer,default=0)
    last_claim_1 = Column(DateTime, default=datetime.now() - timedelta(days=2))
    last_claim_2 = Column(DateTime, default=datetime.now() - timedelta(days=2))
    last_claim_3 = Column(DateTime, default=datetime.now() - timedelta(days=2))
    owner = Column(Integer, default= 0)
    clan_id = Column(Integer, ForeignKey('clans.id'), index=True, nullable= True)

    boosts = relationship('Boost', back_populates='user')


class Boost(Base):
    __tablename__ = 'boost'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tg_id = Column(Integer, ForeignKey('users.tg_id'),unique=True)
    last_watering = Column(DateTime, default=datetime.now() - timedelta(days=2))
    watering_amount = Column(Integer, nullable=False, default=0)
    auto_watering = Column(Integer, nullable=False, default=0)
    garden = Column(Integer, unique=True, default=1)
    amount_ferm = Column(Integer, nullable=True, default=1)

    user = relationship('User', back_populates='boosts')

class Clan(Base):
    __tablename__ = 'clans'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    clan_balance = Column(Integer, nullable=False, default=0)
    clan_collected = Column(Integer, nullable=True, default=0)
    amount_members = Column(Integer, nullable=False, default=1)
    id_owner = Column(Integer, nullable=False)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable= False)
    amount = Column(Integer, nullable=False)
    validate = Column(Integer, default = 0)
    tg_id = Column(Integer, nullable = False)
    url = Column(String, nullable= False)

class TaskDone(Base):
    __tablename__ = 'tasks_done'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    task_id = Column(Integer,  index=True)
    tg_id = Column(Integer,  index=True)
