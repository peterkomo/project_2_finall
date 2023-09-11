# Import necessary libraries for SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for SQLAlchemy models
Base = declarative_base()

# Define the User model
class User(Base):
    # Set the table name
    __tablename__ = 'users'
    
    # Define user-related columns
    user_id = Column(Integer, primary_key=True)
    user_first_name = Column(String(50))
    user_second_name = Column(String(50))
    user_surname = Column(String(50))
    user_login_code = Column(String(10), unique=True)
    role = Column(String(20), default='customer')
    unique_code = Column(String(10))

    # Define relationships for User
    cart_items = relationship('Shopping_Cart', back_populates='user')
    orders = relationship('Order', back_populates='user')

# Define the Product model
class Product(Base):
    # Set the table name
    __tablename__ = 'products'

    # Define product-related columns
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    quantity = Column(Integer)
    price = Column(Float)
    pickup_point_id = Column(Integer, ForeignKey('pickup_points.id'))
    
    # Define a relationship to PickupPoint
    pickup_point = relationship("PickupPoint")
    
    # Define a one-to-many relationship with Shopping_Cart
    cart_entries = relationship("Shopping_Cart", back_populates="product")

# Define the Shopping_Cart model
class Shopping_Cart(Base):
    # Set the table name
    __tablename__ = 'shopping_cart'

    # Define cart-related columns
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    quantity = Column(Integer)
    
    # Define relationships for Shopping_Cart
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_entries")
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order", back_populates="cart_entries")

# Define the PickupPoint model
class PickupPoint(Base):
    # Set the table name
    __tablename__ = 'pickup_points'

    # Define pickup point-related columns
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    address = Column(String(200))
    contact = Column(String(100))

# Define the Order model
class Order(Base):
    # Set the table name
    __tablename__ = 'orders'

    # Define order-related columns
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    delivery_location = Column(String(200))
    
    # Define relationships for Order
    user = relationship("User", back_populates="orders")
    cart_entries = relationship("Shopping_Cart", back_populates="order")

# Create a SQLite database engine and create tables
engine = create_engine('sqlite:///unclepetesgrocery.db')
Base.metadata.create_all(engine)

# Create a session for interacting with the database
Session = sessionmaker(bind=engine)
session = Session()

# Define a function to create a new user
def create_new_user():
    # Prompt the user for user details
    print("Please add your details:")
    usr_fn = input("First Name: ")
    usr_sn = input("Second Name: ")
    usr_uc = input("Surname: ")
    usr_lc = input("Login Code: ")

    # Create a new User object and add it to the session
    new_user = User(user_first_name=usr_fn, user_second_name=usr_sn, user_surname=usr_uc, user_login_code=usr_lc)
    session.add(new_user)
    session.commit()

    # Generate a unique code and update the user's unique_code field
    user = session.query(User).filter_by(user_login_code=usr_lc).first()  
    new_user_code = f"s{usr_fn[0]}{usr_sn[0]}{user.user_id}{usr_uc[-1]}"
    user.unique_code = new_user_code
    session.commit()

    # Print a confirmation message
    print(f"Thank you for registering with us. Your login code is {usr_lc}")

# Define a function to create a new product
def create_product():
    # Prompt the user for product details
    print("Please add product details:")
    product_name = input("Product Name: ")
    product_quantity = int(input("Product Quantity: "))
    product_price = float(input("Product Price: "))

    # Create a new Product object and add it to the session
    new_product = Product(name=product_name, quantity=product_quantity, price=product_price)
    session.add(new_product)
    session.commit()

    # Print a confirmation message
    print(f"Product {product_name} with quantity {product_quantity} and price ${product_price:.2f} has been created.")

# Define a function to add dummy pickup points to the database
def add_dummy_pickup_points():
    dummy_pickup_points = [
        {"name": "Store A", "address": "kabiria", "contact": "Phone: 0790959845"},
        {"name": "Store B", "address": "korogocho", "contact": "Phone: 0736342027"},
    ]

    for point_info in dummy_pickup_points:
        # Create PickupPoint objects for dummy pickup points and add them to the session
        pickup_point = PickupPoint(name=point_info["name"], address=point_info["address"], contact=point_info["contact"])
        session.add(pickup_point)

    session.commit()

# Define a function to add dummy products to the database
def add_dummy_products():
    # Define pickup points for dummy products
    store_a = PickupPoint(name="Store A", address="kabiria", contact="Phone: 0790959845")
    store_b = PickupPoint(name="Store B", address="korogocho", contact="Phone: 0736342027")

    dummy_products = [
        {"name": "Apple", "quantity": 100, "price": 1.00, "pickup_point": store_a},
        {"name": "Banana", "quantity": 50, "price": 0.75, "pickup_point": store_b},
        {"name": "Orange", "quantity": 75, "price": 1.25, "pickup_point": store_a},
    ]

    for product_info in dummy_products:
        # Create Product objects for dummy products and add them to the session
        product = Product(name=product_info["name"], quantity=product_info["quantity"], price=product_info["price"], pickup_point=product_info["pickup_point"])
        session.add(product)

    session.commit()

# Define a function to view the shopping cart for a user
def view_shopping_cart(user):
    print(f"Shopping Cart for {user.user_first_name} {user.user_surname}:")
    # Query the database for cart entries associated with the user
    cart_entries = session.query(Shopping_Cart).filter_by(user_id=user.user_id).all()

    if not cart_entries:
        print("Your shopping cart is empty.")
    else:
        total_cost = 0
        for cart_entry in cart_entries:
            product = cart_entry.product
            subtotal = cart_entry.quantity * product.price
            total_cost += subtotal
            print(f"Product: {product.name}, Quantity: {cart_entry.quantity}, Subtotal: ${subtotal:.2f}")

        print(f"Total Cost: ${total_cost:.2f}")

        # Ask the user if they want to place an order
        place_order_option = input("Do you want to place an order? (yes/no): ").strip().lower()
        if place_order_option == "yes":
            delivery_location = input("Enter the delivery location: ")
            place_order(user, total_cost, delivery_location)
        else:
            print("Order not placed. Returning to the main menu.")

# Define a function to place an order for a user
def place_order(user, total_cost, delivery_location):
    till_number = "12458"  # Simulated till number
    print(f"Order placed successfully! Your till number is: {till_number}")
    clear_shopping_cart(user)
    print(f"Your order will be delivered to: {delivery_location}")
    print("Thanks for shopping with us!")

# Define a function to clear the shopping cart for a user
def clear_shopping_cart(user):
    # Delete all cart entries associated with the user
    session.query(Shopping_Cart).filter_by(user_id=user.user_id).delete()
    session.commit()

# Define a function to display the shopping menu for a user
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

# Define a function to browse and add products to the shopping cart
def browse_products(user):
    print("\nAvailable Products:")
    # Query the database for available products
    products = session.query(Product).all()

    if not products:
        print("No products available.")
        return

    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Quantity: {product.quantity}, Price: ${product.price:.2f}, Pick-up Point: {product.pickup_point.name}")

    while True:
        product_id = input("Enter the ID of the product you want to add to your cart (0 to exit): ")

        if product_id == "0":
            return
        elif not product_id.isdigit():
            print("Invalid input. Please enter a valid product ID.")
            continue

        product_id = int(product_id)

        product = session.query(Product).filter_by(id=product_id).first()
        if product:
            while True:
                quantity = input("Enter the quantity: ")

                if not quantity.isdigit():
                    print("Invalid input. Please enter a valid quantity.")
                    continue

                quantity = int(quantity)

                if quantity <= 0:
                    print("Quantity must be greater than 0.")
                elif quantity > product.quantity:
                    print("Insufficient quantity available.")
                else:
                    add_to_shopping_cart(user, product, quantity)
                    print(f"{quantity} {product.name} added to your shopping cart.")
                    break
        else:
            print("Product not found. Please enter a valid product ID.")

# Define a function to add products to the shopping cart
def add_to_shopping_cart(user, product, quantity):
    cart_entry = session.query(Shopping_Cart).filter_by(user_id=user.user_id, product_id=product.id).first()

    if cart_entry:
        cart_entry.quantity += quantity
    else:
        new_cart_entry = Shopping_Cart(user=user, product=product, quantity=quantity)
        session.add(new_cart_entry)

    session.commit()

# Define the main function for user interaction
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
