from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from settings import MYSQL_DB_URI

# declare a Mapping,this is the class describe map to table column
Base = declarative_base()

engine = create_engine(MYSQL_DB_URI)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


@contextmanager
def scoped_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.remove()


class Cnbeta(Base):
    __tablename__ = 'cnbeta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Integer, nullable=False, default=0)
    catid = Column(Integer, nullable=False, default=0)
    score_story = Column(String(512), nullable=False, default='')
    hometext = Column(String(1024), nullable=False, default='')
    counter = Column(Integer, nullable=False, default=0)
    inputtime = Column(DateTime, nullable=False, default=datetime.now())
    topic = Column(Integer, nullable=False, default=0)
    source = Column(String(128), nullable=False, default='')
    mview = Column(Integer, nullable=False, default=0)
    comments = Column(Integer, nullable=False, default=0)
    crawled_datetime = Column(DateTime, nullable=False, default=datetime.now())
    rate_sum = Column(Integer, nullable=False, default=0)
    title = Column(String(512), nullable=False, default='')
    url_show = Column(String(512), nullable=False, default='')
    thumb = Column(String(256), nullable=False, default='')


def map_orm_item(scrapy_item, sql_item):
    for k, v in scrapy_item.iteritems():
        sql_item.__setattr__(k, v)
    return sql_item


