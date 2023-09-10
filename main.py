from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
#importng nessesary libraries

Base = declarative_base()
#declarative base for sql alchemy

class User(Base):# users class defining user table 
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_first_name = Column(String(50))
    user_second_name = Column(String(50))
    user_surname = Column(String(50))
    user_email = Column(String(100), unique=True)
    role = Column(String(20), default='customer')
    unique_code = Column(String(10))

cart_items = relationship('Shopping_Cart', back_populates='user')
orders = relationship('Order', back_populates='user')
#established one tomany relationships

#product table
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    quantity = Column(Integer)
    price = Column(Float)
    #
    # foreign key reference to PickupPoint
    pickup_point_id = Column(Integer, ForeignKey('pickup_points.id'))
    pickup_point = relationship("PickupPoint")

    #one to many relationship with shoppng cart
    cart_entries = relationship("Shopping_Cart", back_populates="product")

#shopping cart table
class Shopping_Cart(Base):
    __tablename__ = 'shopping_cart'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    quantity = Column(Integer)

    
    #established relationships
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_entries")
    order_id = Column(Integer, ForeignKey('orders.id'))  # Add a foreign key reference to Order
    order = relationship("Order", back_populates="cart_entries")

#pickup point table
class PickupPoint(Base):
        __tablename__ = 'pickup_points'
        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        address = Column(String(200))
        contact = Column(String(100))
#table for order
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    delivery_location = Column(String(200))  

    #relationships
    user = relationship("User", back_populates="orders")
    cart_entries = relationship("Shopping_Cart", back_populates="order")







