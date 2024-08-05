import json
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
                CREATE TABLE IF NOT EXISTS countries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    country_name VARCHAR(255) NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS regions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    region_name VARCHAR(255) NOT NULL,
                    country_id INT,
                    parent_region_id INT NULL,
                    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE,
                    FOREIGN KEY (parent_region_id) REFERENCES regions(id) ON DELETE CASCADE
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

    def populate_from_json(self, json_file_path):
        if not self.connection or not self.connection.is_connected():
            print("Connection to the database failed. Cannot populate tables.")
            return

        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                region_data = json.load(file)

            cursor = self.connection.cursor()

            # Insert countries, regions, and subregions
            for country, regions in region_data.items():
                # Insert country
                cursor.execute("INSERT INTO countries (country_name) VALUES (%s)", (country,))
                country_id = cursor.lastrowid
                print(f"Inserted country: {country} with ID: {country_id}")

                for region, subregions in regions.items():
                    # Insert top-level region
                    cursor.execute("INSERT INTO regions (region_name, country_id, parent_region_id) VALUES (%s, %s, NULL)", (region, country_id))
                    region_id = cursor.lastrowid
                    print(f"Inserted region: {region} with ID: {region_id}")

                    # Insert subregions if any
                    if isinstance(subregions, dict):
                        for subregion, microregions in subregions.items():
                            cursor.execute("INSERT INTO regions (region_name, country_id, parent_region_id) VALUES (%s, %s, %s)", (subregion, country_id, region_id))
                            subregion_id = cursor.lastrowid
                            print(f"Inserted subregion: {subregion} under region ID: {region_id}")

                            # Insert microregions if any
                            if isinstance(microregions, list):
                                for microregion in microregions:
                                    cursor.execute("INSERT INTO regions (region_name, country_id, parent_region_id) VALUES (%s, %s, %s)", (microregion, country_id, subregion_id))
                                    print(f"Inserted microregion: {microregion} under subregion ID: {subregion_id}")
                    elif isinstance(subregions, list):
                        for subregion in subregions:
                            cursor.execute("INSERT INTO regions (region_name, country_id, parent_region_id) VALUES (%s, %s, %s)", (subregion, country_id, region_id))
                            print(f"Inserted subregion: {subregion} under region ID: {region_id}")

            self.connection.commit()
            print("Data inserted successfully into countries, regions, and subregions tables")

        except Error as e:
            print(f"Error while populating tables: {e}")


    def get_all_wines(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT w.name, t.type_name, w.year, r.region_name, w.price, w.quantity 
                FROM wines w
                JOIN types t ON w.type_id = t.id
                JOIN regions r ON w.region_id = r.id
            """)
            wines = cursor.fetchall()
            cursor.close()
            return wines
        except Error as e:
            print(f"Error fetching wines: {e}")
            return []
            
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

# Example of using the Database class to create tables and populate from JSON
if __name__ == "__main__":
    db = Database()
    db.create_tables()
    db.populate_from_json('webScraper/wine_regions.json')
    db.close_connection()
