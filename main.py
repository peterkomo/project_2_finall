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


#prompts the user to place oreds and  a series of questions on it
def place_order(user, total_cost, delivery_location):
    till_number = "12458"
    print(f"Order placed successfully! Your till number is: {till_number}")
    clear_shopping_cart(user)
    print(f"Your order will be delivered to: {delivery_location}")
    print("Thanks for shopping with us!")


#enable user to clear shopping cart
def clear_shopping_cart(user):
    session.query(Shopping_Cart).filter_by(user_id=user.user_id).delete()
    session.commit()

def shopping_menu(user):
    while True:
        print("\nShopping Menu:")
        print("1. Browse Products")
        print("2. View Shopping Cart")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            browse_products(user)
        elif choice == "2":
            view_shopping_cart(user)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please choose a valid option.")    

def browse_products(user):
    # Display a header for available products
    print("\nAvailable Products:")
    
    # Retrieve all products from the database
    products = session.query(Product).all()

    # Check if there are no products available
    if not products:
        print("No products available.")
        return

    # Iterate through each product and display its details
    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Quantity: {product.quantity}, Price: ${product.price:.2f}, Pick-up Point: {product.pickup_point.name}")

    # Create an infinite loop to allow the user to select products to add to the cart
    while True:
        # Prompt the user to enter the ID of the product they want to add to the cart
        product_id = input("Enter the ID of the product you want to add to your cart (0 to exit): ")

        # Check if the user wants to exit (0)
        if product_id == "0":
            return
        
        # Check if the input is not a valid integer
        elif not product_id.isdigit():
            print("Invalid input. Please enter a valid product ID.")
            continue

        # Convert the product ID to an integer
        product_id = int(product_id)

        # Retrieve the product from the database based on the entered ID
        product = session.query(Product).filter_by(id=product_id).first()
        
        # Check if the product exists
        if product:
            # Create an inner loop to allow the user to specify the quantity of the product
            while True:
                # Prompt the user to enter the quantity
                quantity = input("Enter the quantity: ")

                # Check if the input is not a valid integer
                if not quantity.isdigit():
                    print("Invalid input. Please enter a valid quantity.")
                    continue

                # Convert the quantity to an integer
                quantity = int(quantity)

                # Check if the entered quantity is valid
                if quantity <= 0:
                    print("Quantity must be greater than 0.")
                elif quantity > product.quantity:
                    print("Insufficient quantity available.")
                else:
                    # Call the 'add_to_shopping_cart' function to add the product to the user's cart
                    add_to_shopping_cart(user, product, quantity)
                    print(f"{quantity} {product.name} added to your shopping cart.")
                    break
        else:
            print("Product not found. Please enter a valid product ID.")

def add_to_shopping_cart(user, product, quantity):
    # Check if the same product is already in the user's shopping cart
    cart_entry = session.query(Shopping_Cart).filter_by(user_id=user.user_id, product_id=product.id).first()

    if cart_entry:
        # If the product is already in the cart, update the quantity
        cart_entry.quantity += quantity
    else:
        # If the product is not in the cart, create a new cart entry for the user
        new_cart_entry = Shopping_Cart(user=user, product=product, quantity=quantity)
        session.add(new_cart_entry)

    # Commit the changes to the database, saving the updated shopping cart
    session.commit()


def main():
    print("Welcome to Uncle Pete's groceries system")
    print("Are you an existing member?")
    print("1. Yes")
    print("2. No")

    get_choice = input("Choose one: ")

    if get_choice == "1":
        usr_lc = input("Please enter your login code: ")
        user = session.query(User).filter_by(user_login_code=usr_lc).first()
        if user:
            print(f"Welcome back, {user.user_first_name}!")
            shopping_menu(user)
        else:
            print("User not found.")
    elif get_choice == "2":
        create_new_user()
    else:
        print("Invalid choice. Please choose 1 or 2.")

if __name__ == "__main__":
    add_dummy_pickup_points()
    add_dummy_products()
    main()












