import mysql.connector
from mysql.connector import Error

def check_tables():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='wine_inventory',
            user='wine_user',
            password='Password#2233'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # Check the countries table
            cursor.execute("SELECT * FROM countries LIMIT 10;")
            countries = cursor.fetchall()
            print("Countries Table:")
            for row in countries:
                print(row)

            # Check the regions table
            cursor.execute("SELECT * FROM regions LIMIT 10;")
            regions = cursor.fetchall()
            print("\nRegions Table:")
            for row in regions:
                print(row)

            # Check the wines table
            cursor.execute("SELECT * FROM wines LIMIT 10;")
            wines = cursor.fetchall()
            print("\nWines Table:")
            for row in wines:
                print(row)

            # Check the types table
            cursor.execute("SELECT * FROM types LIMIT 10;")
            types = cursor.fetchall()
            print("\nTypes Table:")
            for row in types:
                print(row)

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    check_tables()
