from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
#importng nessesary libraries

Base = declarative_base()
#declarative base for sql alchemy

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_first_name = Column(String(50))
    user_second_name = Column(String(50))
    user_surname = Column(String(50))
    user_login_code = Column(String(10), unique=True)  # Change from user_email to user_login_code
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

engine = create_engine('sqlite:///unclepetesglosary.db')
Base.metadata.create_all(engine)# cratin class definations to intaract with the clas es
Session = sessionmaker(bind=engine)
session = Session()# session maker to connect with engene


def create_new_user():
    print("Please add your details:")
    usr_fn = input("First Name: ")
    usr_sn = input("Second Name: ")
    usr_uc = input("Surname: ")
    usr_lc = input("Login Code: ")

    new_user = User(user_first_name=usr_fn, user_second_name=usr_sn, user_surname=usr_uc, user_login_code=usr_lc)
    session.add(new_user)
    session.commit()

    #his line of code constructs a User object with the user's personal information and login code.







