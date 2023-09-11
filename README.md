# project_2_finall
# Uncle Pete's Grocery System

Welcome to Uncle Pete's Grocery System! This is a Python application that manages an online grocery store. Customers can browse products, add them to their shopping cart, and place orders for delivery. Additionally, it supports user registration and maintains a database of products, users, orders, and pickup points.

## Table of Contents

- [Getting Started](#getting-started)
- [Models](#models)
- [Functions](#functions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Getting Started

### Prerequisites

To run this application, you'll need Python installed on your system. You can download and install Python from the [official Python website](https://www.python.org/downloads/).

### Installation

Clone the GitHub repository for this project:

```bash
git clone https://github.com/peterkomo/project_2_finall
```

Navigate to the project directory:

```bash
cd project_2_finall
```

install dependancies ..pipfiles and sql alchemy
enter the enviroment to runn the codes

## MODELS
The application uses SQLAlchemy to define the following data models:
# USER MODELS
- user_id: Unique identifier for the user.
- user_first_name: First name of the user.
- user_second_name: Second name of the user.
- user_surname: Surname of the user.
- user_login_code: Unique login code for the user.
- role: User role (default is 'customer').
- unique_code: Unique code generated for the user.

# PRODUCT MODEL

- id: Unique identifier for the product.
- name: Name of the product.
- quantity: Available quantity of the product.
- price: Price of the product.
- pickup_point_id: Identifier for the pickup point associated with the product.
##  Shopping Cart Model
- id: Unique identifier for the cart entry.
- product_id: Identifier for the product in the cart.
- user_id: Identifier for the user who owns the cart.
- quantity: Quantity of the product in the cart.
- order_id: Identifier for the order (if placed).
# Pickup Point Model
- id: Unique identifier for the pickup point.
- name: Name of the pickup point.
- address: Address of the pickup point.
- contact: Contact information for the pickup point.
# Order Model
- id: Unique identifier for the order.
- user_id: Identifier for the user who placed the order.
- delivery_location: Location for order delivery.
# Functions
The application provides various functions to interact with the database and perform actions like user registration, browsing products, adding products to the shopping cart, viewing the shopping cart, and placing orders.

- create_new_user(): Allows a new user to register.
-create_product(): Enables the addition of a new product to the database.
- add_dummy_pickup_points(): Adds dummy pickup points to the database.
- add_dummy_products(): Adds dummy products to the database.
- view_shopping_cart(user): Displays the shopping cart for a user.
- place_order(user, total_cost, delivery_location): Places an order for a user.
- clear_shopping_cart(user): Clears the shopping cart for a user.
- shopping_menu(user): Displays the shopping menu for a user.
- browse_products(user): Allows users to browse and add products to the shopping cart.
- add_to_shopping_cart(user, product, quantity): Adds products to the shopping cart.
- main(): The main function for user interaction.
# Usage
To run the application, execute the following command:
on the shell run;
```shell
python3 main.py
```
# Licence
MIT License

Copyright (c) 2023 peterkomo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


