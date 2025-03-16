from sqlalchemy import BigInteger, String, ForeignKey, Column, Integer, Date, Time, Boolean, MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from src.config import DATABASE_URL

engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData()
    pass


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, unique=True)
    user_name = Column(String)
    time_zone = Column(String, default='MSK+0')


class Notice(Base):
    __tablename__ = 'Notices'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    name_notice = Column(String)
    day_before = Column(Integer)
    time_send = Column(Time)
    creator = Column(String)


class Payment(Base):
    __tablename__ = 'Payments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    notice_id = Column(Integer, ForeignKey('Notices.id'), default=None)
    name_payment = Column(String)
    cost_payment = Column(Integer)
    payment_day = Column(Integer)

#
# async def async_main():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#         print('database is active')
