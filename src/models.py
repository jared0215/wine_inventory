import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='wine_inventory',
                user='wine_user',
                password='Password#2233'
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def create_tables(self):
        if not self.connection or not self.connection.is_connected():
            print("Connection to the database failed. Tables cannot be created.")
            return
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS types (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    type_name VARCHAR(50) NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS regions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    region_name VARCHAR(100) NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wines (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    type_id INT,
                    year INT,
                    price DECIMAL(10, 2),
                    quantity INT,
                    region_id INT,
                    FOREIGN KEY (type_id) REFERENCES types(id),
                    FOREIGN KEY (region_id) REFERENCES regions(id)
                )
            """)
            self.connection.commit()
            print("Tables created successfully")
        except Error as e:
            print(f"Error while creating tables: {e}")

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

# Example of using the Database class to create tables
if __name__ == "__main__":
    db = Database()
    db.create_tables()
    db.close_connection()
