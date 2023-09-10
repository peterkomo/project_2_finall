from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
#importng nessesary libraries

Base = declarative_base()
#declarative base for sql alchemy

cart_items = relationship('Shopping_Cart', back_populates='user')
orders = relationship('Order', back_populates='user')
#established one tomany relationships