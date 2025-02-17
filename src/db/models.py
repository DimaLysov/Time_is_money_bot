from sqlalchemy import BigInteger, String, ForeignKey, Column, Integer, Date, Time
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from src.config import DATABASE_URL

engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, unique=True)
    user_name = Column(String)


class Notice(Base):
    __tablename__ = 'Notices'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    day_before = Column(Date)
    time_send = Column(Time)
    periodicity = Column(Time)


class Payment(Base):
    __tablename__ = 'Payments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    notifications_id = Column(Integer, ForeignKey('Notices.id'), default=None)
    name_payment = Column(String)
    cost_payment = Column(Integer)
    payment_date = Column(Integer)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print('database is active')
