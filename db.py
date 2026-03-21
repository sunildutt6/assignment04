import mysql.connector
from flask import current_app

def get_db_connection():
    conn = mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DATABASE']
    )
    return conn

def get_single_user():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT userId, name, email, role FROM Users LIMIT 1"
    cursor.execute(query)
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user

def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT p.productId, p.name, p.price, p.stock, c.name AS category
    FROM Products p
    JOIN Categories c ON p.categoryId = c.categoryId
    """
    cursor.execute(query)
    products = cursor.fetchall()

    cursor.close()
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        p.productId,
        p.name,
        p.price,
        p.stock,
        c.name AS category
    FROM Products p
    JOIN Categories c ON p.categoryId = c.categoryId
    WHERE p.productId = %s
    """
    cursor.execute(query, (product_id,))
    product = cursor.fetchone()

    cursor.close()
    conn.close()
    return product

def get_all_categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT categoryId, name FROM Categories"
    cursor.execute(query)
    categories = cursor.fetchall()

    cursor.close()
    conn.close()
    return categories

def insert_category(name):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO Categories (name) VALUES (%s)"
    cursor.execute(query, (name,))
    conn.commit()

    cursor.close()
    conn.close()

def insert_product(name, price, stock, categoryId):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Products (name, price, stock, categoryId)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (name, price, stock, categoryId))
    conn.commit()

    cursor.close()
    conn.close()