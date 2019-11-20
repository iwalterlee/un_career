# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from sqlalchemy import create_engine,Column,Integer,String,Table,MetaData,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Scrapy4Pipeline(object):
    def __init__(self):
        self.engine = create_engine(os.getenv('DBADDRESS'), max_overflow=5)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base = declarative_base()
        self.UnNow = type('un_opp',(Base,UnNow),{'__tablename__':'UN_Now'})
        self.UnHistory = type('un_opp',(Base,UnHistory),{'__tablename__':'UN_History'})

    def open_spider(self, spider):
        self.UnNow.__table__.drop(self.engine)
        self.UnNow.__table__.create(self.engine)

    def process_item(self, item, spider):
        print("pipeline")
        print("-------"*20)
        self.session.add(self.UnNow(**item))
        if self.session.query(self.UnHistory).filter_by(link=item["link"]).scalar() == None:
            self.session.add(self.UnHistory(**item))
        self.session.commit()
        return item

    def close_spider(self,spider):
        self.session.close()


class UnNow():
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    link = Column(String(256))
    level = Column(String(10))
    job_network = Column(String(256))
    job_family = Column(String(256))
    department = Column(String(256))
    location = Column(String(256))
    deadline = Column(Date())
    def __init__(self, **items):
        for key in items:
            if hasattr(self,key):
                setattr(self,key,items[key])

class UnHistory():
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    link = Column(String(256), unique=True)
    level = Column(String(10))
    job_network = Column(String(256))
    job_family = Column(String(256))
    department = Column(String(256))
    location = Column(String(256))
    deadline = Column(Date())
    update_date = Column(Date())
    def __init__(self, **items):
        for key in items:
            if hasattr(self,key):
                setattr(self,key,items[key])
