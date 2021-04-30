from sqlalchemy import create_engine, Integer, JSON, Column, Sequence, Text, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import update, insert, delete, MetaData
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship


import flask
from flask import request, jsonify
import sqlite3


EntityBase = declarative_base()


# class Item(EntityBase):
#     __tablename__ = "items"
#     id = Column(Integer, Sequence("item_id_seq"), primary_key=True, nullable=False)
#     information = Column(JSON, nullable=True)

# class Api(EntityBase):
#     __tablename__ = "api"
#     id = Column(Integer, Sequence("api_id_seq"), primary_key=True, nullable=False)
#     domain = Column(Text, nullable=False)
#     request = Column(JSON, nullable=True)
#     response = Column(JSON, nullable=True)


# class domain(EntityBase):
#     __tablename__ = 'domain'
#     id = Column(Integer, primary_key=True)
#     domain = Column(Text, nullable=True)
#     children = relationship("test", back_populates="parent")

class test(EntityBase):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    information = Column(JSON, nullable=True)
    parent_id = Column(Integer, nullable=True)



# Setup a database connection. Using in-memory database here.
engine = create_engine("sqlite:///GET_API_DATABASE.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables derived from the EntityBase object
EntityBase.metadata.create_all(engine)

#########Declare a new row 
# first_item = test()
# first_item.parent_id = 1
# first_item.information = dict(a=1, b="foo", c=[1, 1, 2, 3, 5, 8, 13])
# session.add(first_item)
# session.commit()

# for i in range(1):
#     second_item = Api()
#     second_item.domain = "quangtest"
#     second_item.request = dict(a=2,b="request", c=[1, 1, 2, 3, 5, 8, 13] )
#     second_item.response = dict(a=2,b="response", c=[1, 1, 2, 3, 5, 8, 13] )
#     session.add(second_item)
#     session.commit()  
  

#######Delete data in table of database
# conn = engine.connect()
# stmt_update = (
#     update(Item).
#     where(Item.id == 5).
#     values(information=None)
# )
# stmt_delete = (
#     delete(Api).
#     where(Api.id != 0)
# )
# conn.execute(stmt_delete)


####Drop table of database
table = 'API'
command = "DROP TABLE IF EXISTS {};".format(table)
conn = sqlite3.connect('GET_API_DATABASE.db')
cur = conn.cursor()
cur.execute(command)
conn.commit()

# Insert it into the database


# # Get all saved items from the database
# for item in session.query(Item).all():
#     print(type(item.information))
#     # <class 'dict'>
#     print(item.id, item.information)
#     # 1 {'a': 1, 'b': 'foo', 'c': [1, 1, 2, 3, 5, 8, 13]}
