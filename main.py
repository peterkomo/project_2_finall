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

    user = session.query(User).filter_by(user_login_code=usr_lc).first()  
    new_user_code = f"s{usr_fn[0]}{usr_sn[0]}{user.user_id}{usr_uc[-1]}"
    user.unique_code = new_user_code
    session.commit()
   # retrieve a user based on their login code, generate a unique code for that user, update the user's unique code in the database, and then commit the changes to the database to persist the updated unique code for that user.
    print(f"Thank you for registering with us. Your login code is {usr_lc}") 
    
def create_product():
    # Prompt the user to enter details for a new product.
    print("Please add product details:")

    # Get the product name from the user and store it in the product_name variable.
    product_name = input("Product Name: ")

    # Get the product quantity from the user and convert it to an integer, storing it in product_quantity.
    product_quantity = int(input("Product Quantity: "))

    # Get the product price from the user and convert it to a float, storing it in product_price.
    product_price = float(input("Product Price: "))

    # Create a new Product object with the provided name, quantity, and price.
    new_product = Product(name=product_name, quantity=product_quantity, price=product_price)

    # Add the new_product to the database session for later insertion into the database.
    session.add(new_product)

    # Commit the changes made in the session to save the new product in the database.
    session.commit()

    # Display a confirmation message with the details of the newly created product.
    print(f"Product {product_name} with quantity {product_quantity} and price ${product_price:.2f} has been created.")
 
def add_dummy_pickup_points():
    # Define a list of dummy pickup point information as dictionaries.
    dummy_pickup_points = [
        {"name": "Store A", "address": "ngong depot", "contact": "Phone: 0756349023"},
        {"name": "Store B", "address": "rabai depot", "contact": "Phone: 0756342034"},
    ]

    # Iterate over each dictionary in the list.
    for point_info in dummy_pickup_points:
        # Create a new PickupPoint object using the information from the current dictionary.
        pickup_point = PickupPoint(name=point_info["name"], address=point_info["address"], contact=point_info["contact"])

        # Add the new pickup_point to the database session.
        session.add(pickup_point)

    # Commit the changes made in the session to save the pickup points in the database.
    session.commit()

def add_dummy_products():
    # Define two pickup points representing stores
    store_a = PickupPoint(name="Store A", address="123 Main St", contact="Phone: (123) 456-7890")
    store_b = PickupPoint(name="Store B", address="456 Elm St", contact="Phone: (987) 654-3210")

    # Define a list of dictionaries with product information
    dummy_products = [
        {"name": "Apple", "quantity": 100, "price": 1.00, "pickup_point": store_a},
        {"name": "Banana", "quantity": 50, "price": 0.75, "pickup_point": store_b},
        {"name": "Orange", "quantity": 75, "price": 1.25, "pickup_point": store_a},
    ]

    # Loop through the list of dummy products
    for product_info in dummy_products:
        # Create a Product object for each product
        product = Product(name=product_info["name"], quantity=product_info["quantity"],
                          price=product_info["price"], pickup_point=product_info["pickup_point"])

        # Add the product to the current session
        session.add(product)

    # Commit the changes to the database
    session.commit()


def view_shopping_cart(user):
    # Print the user's shopping cart header
    print(f"Shopping Cart for {user.user_first_name} {user.user_surname}:")

    # Query the database for cart entries associated with the user
    cart_entries = session.query(Shopping_Cart).filter_by(user_id=user.user_id).all()

    # Check if the shopping cart is empty
    if not cart_entries:
        print("Your shopping cart is empty.")
    else:
        total_cost = 0

        # Loop through each cart entry and display product information
        for cart_entry in cart_entries:
            product = cart_entry.product
            subtotal = cart_entry.quantity * product.price
            total_cost += subtotal

            # Print product details and subtotal for each item in the cart
            print(f"Product: {product.name}, Quantity: {cart_entry.quantity}, Subtotal: ${subtotal:.2f}")

        # Display the total cost of items in the shopping cart
        print(f"Total Cost: ${total_cost:.2f}")

        # Ask the user if they want to place an order
        place_order_option = input("Do you want to place an order? (yes/no): ").strip().lower()
        
        # If the user chooses to place an order, prompt for the delivery location
        if place_order_option == "yes":
            delivery_location = input("Enter the delivery location: ")
            place_order(user, total_cost, delivery_location)
        else:
            # If the user chooses not to place an order, inform them and return to the main menu
            print("Order not placed. Returning to the main menu.")











