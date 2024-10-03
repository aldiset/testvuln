import sqlite3

# Create a connection to the SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('database.db')

# Create a cursor object using the connection
cursor = conn.cursor()

# SQL query to create the products table with detailed columns
create_products_table_query = '''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT NOT NULL
);
'''

# SQL query to create the users table with detailed columns
create_users_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
'''

# Execute the query to create the tables
cursor.execute(create_products_table_query)
cursor.execute(create_users_table_query)

# SQL query to insert detailed product data into the products table
insert_products_data_query = '''
INSERT INTO products (name, price, description)
VALUES
    ('Laptop', 999.99, 'A high-performance laptop with 16GB RAM and 512GB SSD.'),
    ('Smartphone', 499.99, 'A 5G smartphone with a stunning OLED display and 128GB storage.'),
    ('Tablet', 299.99, 'A lightweight tablet with a 10-inch display and 64GB storage.'),
    ('Headphones', 149.99, 'Wireless noise-cancelling headphones with long battery life.'),
    ('Smartwatch', 199.99, 'A sleek smartwatch with fitness tracking and heart rate monitoring.');
'''

# SQL query to insert user data into the users table
insert_users_data_query = '''
INSERT INTO users (fullname, username, email, password)
VALUES
    ('John Doe', 'john_doe', 'john_doe@example.com', 'password123'),
    ('Jane Smith', 'jane_smith', 'jane_smith@example.com', 'mysecurepassword'),
    ('Alice Wonder', 'alice_wonder', 'alice_wonder@example.com', 'alicepassword');
'''

# Execute the queries to insert data
cursor.execute(insert_products_data_query)
cursor.execute(insert_users_data_query)

# Commit the changes to the database
conn.commit()

# Fetch all data from the products table to verify the insertions
cursor.execute('SELECT * FROM products')
products_rows = cursor.fetchall()

# Display the fetched data from the products table
print("Product List:")
print("ID | Name         | Price    | Description")
print("----------------------------------------------")
for row in products_rows:
    print(f'{row[0]:<2} | {row[1]:<12} | ${row[2]:<7.2f} | {row[3]}')

# Fetch all data from the users table to verify the insertions
cursor.execute('SELECT * FROM users')
users_rows = cursor.fetchall()

# Display the fetched data from the users table
print("\nUser List:")
print("ID | Full Name     | Username     | Email")
print("----------------------------------------------")
for row in users_rows:
    print(f'{row[0]:<2} | {row[1]:<12} | {row[2]:<12} | {row[3]}')

# Close the connection to the database
conn.close()
