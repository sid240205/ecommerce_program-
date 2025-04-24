from faker import Faker
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta

fake = Faker()

class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")

    # def disconnect(self):
    #     if self.connection:
    #         self.connection.close()
    #         print("Disconnected from MySQL database")

    def disconnect(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
            print("Disconnected from MySQL database")


class CustomerGenerator:
    def __init__(self):
        self.customers = []

    def generate_customers(self, count):
        for _ in range(count):
            customer = {
            'customer_id': fake.uuid4(),
            'customer_zip_code_prefix': fake.zipcode(),  #zip_code
            'customer_city': fake.city(),  # city
            'customer_state': fake.state(),  # state
            'gender': random.choice(['Male', 'Female']),
            'age': random.randint(18, 80)
            }
            self.customers.append(customer)
        return self.customers
    

class OrderItemGenerator:
    def __init__(self, orders, products):
        self.order_items = []
        self.orders = orders
        self.products = products
        
    def generate_order_items(self):
        for order in self.orders:
            items_count = random.randint(1, 5)
            for i in range(items_count):
                product = random.choice(self.products)
                item = {
                    'order_id': order['order_id'],
                    'order_item_id': i+1,
                    'product_id': product['product_id'],
                    'seller_id': fake.uuid4(),
                    'price': round(random.uniform(10, 500), 2),
                    'shipping_charges': round(random.uniform(5, 50), 2)
                }
                self.order_items.append(item)
        return self.order_items

class ProductGenerator:
    def __init__(self):
        self.products = []

    def generate_products(self, count):
        categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Toys']
        for _ in range(count):
            product = {
                'product_id': fake.uuid4(),
                'category': random.choice(categories),
                'weight': random.uniform(100, 5000),
                'length': random.uniform(10, 200),
                'height': random.uniform(5, 100),
                'width': random.uniform(5, 100),
                'cost': round(random.uniform(10, 1000), 2),
                'name': fake.word().capitalize()
            }
            self.products.append(product)
        return self.products

class OrderGenerator:
    def __init__(self, customers):
        self.orders = []
        self.customers = customers

    def generate_orders(self, count):
        statuses = ['delivered', 'cancelled', 'processing']
        for _ in range(count):
            customer = random.choice(self.customers)
            order = {
                'order_id': fake.uuid4(),
                'customer_id': customer['customer_id'],
                'status': random.choice(statuses),
                'purchase_ts': fake.date_time_this_year(),
                'approved_ts': fake.date_time_this_year(),
                'delivered_ts': fake.date_time_this_year(),
                'estimated_date': fake.date_this_year()
            }
            self.orders.append(order)
        return self.orders

class DataFeeder:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def feed_customers(self, customers):
        cursor = self.db_handler.connection.cursor()
        for customer in customers:
            cursor.execute('''
            INSERT INTO Customers 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            customer['customer_id'],
            customer['customer_zip_code_prefix'],
            customer['customer_city'],
            customer['customer_state'],
            customer['gender'],
            customer['age']
        ))
        self.db_handler.connection.commit()
        cursor.close()

    def feed_products(self, products):
        cursor = self.db_handler.connection.cursor()
        for product in products:
            cursor.execute('''
                INSERT INTO Products 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                product['product_id'],
                product['category'],
                product['weight'],
                product['length'],
                product['height'],
                product['width'],
                product['cost'],
                product['name']
            ))
        self.db_handler.connection.commit()
        cursor.close()

    def feed_order_items(self, order_items):
        cursor = self.db_handler.connection.cursor()
        for item in order_items:
            cursor.execute('''
            INSERT INTO Order_Items 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            item['order_id'],
            item['order_item_id'],
            item['product_id'],
            item['seller_id'],
            item['price'],
            item['shipping_charges']
        ))
        self.db_handler.connection.commit()
        cursor.close()

    def feed_orders(self, orders):
        cursor = self.db_handler.connection.cursor()
        for order in orders:
            cursor.execute('''
                INSERT INTO Orders 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                order['order_id'],
                order['customer_id'],
                order['status'],
                order['purchase_ts'],
                order['approved_ts'],
                order['delivered_ts'],
                order['estimated_date']
            ))
        self.db_handler.connection.commit()
        cursor.close()



if __name__ == "__main__":
    db = DatabaseHandler(host='localhost', user='root', password='Oracle2005', database='lit_db')
    db.connect()

    # Generate data
    customer_gen = CustomerGenerator()
    customers = customer_gen.generate_customers(200)  # 200 unique customers

    product_gen = ProductGenerator()
    products = product_gen.generate_products(100)  # 100 products

    order_gen = OrderGenerator(customers)
    orders = order_gen.generate_orders(1000)  # 1000 orders

    # Feed data to MySQL
    feeder = DataFeeder(db)
    feeder.feed_customers(customers)
    feeder.feed_products(products)
    feeder.feed_orders(orders)

    # Populate Order_Items and Customer_Orders similarly (code omitted for brevity)
    order_item_gen = OrderItemGenerator(orders, products)
    order_items = order_item_gen.generate_order_items()
    feeder.feed_order_items(order_items)
    

    db.disconnect()