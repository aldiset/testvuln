import sqlite3

# Create a connection to the SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('database.db')

# Create a cursor object using the connection
cursor = conn.cursor()

# SQL query to create the products table with detailed columns
create_table_query = '''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT NOT NULL
);
'''

# Execute the query to create the table
cursor.execute(create_table_query)

# SQL query to insert detailed product data into the products table
insert_data_query = '''
INSERT INTO products (name, price, description)
VALUES
    ('Laptop', 999.99, 'A high-performance laptop with 16GB RAM and 512GB SSD.'),
    ('Smartphone', 499.99, 'A 5G smartphone with a stunning OLED display and 128GB storage.'),
    ('Tablet', 299.99, 'A lightweight tablet with a 10-inch display and 64GB storage.'),
    ('Headphones', 149.99, 'Wireless noise-cancelling headphones with long battery life.'),
    ('Smartwatch', 199.99, 'A sleek smartwatch with fitness tracking and heart rate monitoring.');
'''

# Execute the query to insert data
cursor.execute(insert_data_query)

# Commit the changes to the database
conn.commit()

# Fetch all data from the products table to verify the insertions
cursor.execute('SELECT * FROM products')
rows = cursor.fetchall()

# Display the fetched data
print("Product List:")
print("ID | Name         | Price    | Description")
print("----------------------------------------------")
for row in rows:
    print(f'{row[0]:<2} | {row[1]:<12} | ${row[2]:<7.2f} | {row[3]}')

# Close the connection to the database
conn.close()
