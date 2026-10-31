import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Creates a table using a given connection
# (Relies on caller to close the connection)
def init_table(conn):
    try:
        cursor = conn.cursor()
        sql_query = ("CREATE TABLE IF NOT EXISTS fruits "
                     "(id INTEGER AUTO_INCREMENT PRIMARY KEY, "
                     "name VARCHAR(255), price INTEGER);")
        cursor.execute(sql_query)
        conn.commit()
        cursor.close()
    except Error as e:
        print(f"Error while creating table: {e}")

# Initializes the database and calls init_table
def init_db():
    load_dotenv()

    db_name = os.environ.get('DB_DATABASE')
    if not db_name:
        raise ValueError("DB_DATABASE is missing from .env")
    admin_user = os.environ.get('DB_USER')
    admin_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST', 'localhost')
    port = int(os.environ.get('DB_PORT', 3306))

    conn = None
    try:

        # Connect to the MySQL server using root
        # (Created admin uses the commented values)
        conn = mysql.connector.connect(
            host='localhost', # os.environ.get('DB_HOST')
            user='root', # os.environ.get('DB_USER')
            password='Rootbeer543!', # os.environ.get('DB_PASSWORD'),
            port=3306  # os.environ.get('DB_PORT')
        )
        
        # Create a cursor to execute queries
        cursor = conn.cursor()

        # Create database (confirm on terminal)
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        cursor.execute(f"USE `{db_name}`;")
        
        print(f"Database '{db_name}' checked/created successfully.")

        # Create user (also confirm on terminal)
        cursor.execute(
            f"CREATE USER IF NOT EXISTS '{admin_user}'@'{db_host}' "
            f"IDENTIFIED BY '{admin_password}';"
        )
        cursor.execute(
            f"GRANT ALL PRIVILEGES ON `{db_name}`.* "
            f"TO '{admin_user}'@'{db_host}';"
        )
        cursor.execute("FLUSH PRIVILEGES;")

        print(f"User '{admin_user}' created successfully.")

        # Initialize the table
        init_table(conn)   # default DB is now db_name
        cursor.close()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if conn is not None and conn.is_connected():
            conn.close()

