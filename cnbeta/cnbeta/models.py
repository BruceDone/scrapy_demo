from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import MYSQL_CONN
from datetime import datetime

# declare a Mapping,this is the class describe map to table column
Base = declarative_base()


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


def create_session():
    # declare the connecting to the server
    engine = create_engine(MYSQL_CONN['mysql_uri']
                           .format(user=MYSQL_CONN['user'], pwd=MYSQL_CONN['password'], host=MYSQL_CONN['host'],
                                   db=MYSQL_CONN['db'])
                           , echo=False)
    # connect session to active the action
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def map_orm_item(scrapy_item,sql_item):
    for k, v in scrapy_item.iteritems():
        sql_item.__setattr__(k, v)
    return sql_item


def convert_date(date_str):
    pass

