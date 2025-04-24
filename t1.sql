use lit_db

CREATE TABLE Customers (
    customer_id VARCHAR(255) PRIMARY KEY,
    customer_zip_code_prefix VARCHAR(10) NOT NULL,
    customer_city VARCHAR(255) NOT NULL,
    customer_state VARCHAR(255) NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    age INT CHECK (age >= 0)
);

CREATE TABLE Products (
    product_id VARCHAR(255) PRIMARY KEY,
    product_category_name VARCHAR(255),
    product_weight_g DECIMAL(10,2),
    product_length_cm DECIMAL(10,2),    
    product_height_cm DECIMAL(10,2),
    product_width_cm DECIMAL(10,2),
    product_cost DECIMAL(10,2),
    product_name VARCHAR(255)
);

CREATE TABLE Orders (
    order_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255),
    order_status VARCHAR(50),
    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME,
    order_delivered_timestamp DATETIME,
    order_estimated_delivery_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE Order_Items (
    order_id VARCHAR(255),
    order_item_id INT,
    product_id VARCHAR(255),
    seller_id VARCHAR(255),
    price DECIMAL(10,2),
    shipping_charges DECIMAL(10,2),
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);


CREATE TABLE Customer_Orders (
    customer_id VARCHAR(255) PRIMARY KEY,
    total_orders INT,
    total_spent DECIMAL(10,2),
    last_order_date DATETIME,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);