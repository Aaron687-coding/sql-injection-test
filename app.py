import mysql.connector
from mysql.connector import Error
# from mysql.connector.constants import ClientFlag # UNCOMMENT FOR MULTI-STATEMENTS
import os
from dotenv import load_dotenv

from init_db import init_db

# Prints the fruits (# and then all rows)
def print_fruits(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM fruits;')
        result = cursor.fetchall()
        print(f"Total number of rows in 'fruits' table: {len(result)}")
        for row in result:
            print(row)
    except Error as e:
        print(f"Error while printing table: {e}")

if __name__ == "__main__":
    load_dotenv()
    init_db()

    conn = None
    # All-encompassing try-catch for connecting + querying
    # (In case the user actually injects something evil)
    try:
        # Use the admin user we set up in init_db
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'), # just random characters
            port=int(os.environ.get('DB_PORT', 3306)),
            database=os.environ.get('DB_DATABASE'),
            # client_flags=[ClientFlag.MULTI_STATEMENTS], # UNCOMMENT FOR MULTI-STATEMENTS
        )

        cursor = conn.cursor()

        # Repeatedly get unsanitized input!
        while True:
            # Print the # of rows in fruitsDB & what the rows are
            print_fruits(conn)

            # Get input from user
            rest_of_query = input(
                "\nAdd row (format \"('name', price)\")\n"
                "INSERT INTO fruits (name, price) VALUES "
            )

            cursor.execute("INSERT INTO fruits (name, price) VALUES " + rest_of_query)
            # UNCOMMENT BELOW FOR MULTI-STATEMENTS
            # while cursor.nextset():      # advance through the extra statements' results
            #     pass
            conn.commit()

            # Ask user if they want to add another value
            if input("Add another value (Y/anything else)? ").lower() != 'y':
                break

        cursor.close()

    except Error as e:
        print(f"Error while connecting to/querying table: {e}")
    finally:
        if conn is not None and conn.is_connected():
            conn.close()