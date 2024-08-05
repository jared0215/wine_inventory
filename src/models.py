import json
import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.INFO)

def ensure_connection(func):
    def wrapper(self, *args, **kwargs):
        if not self.connection or not self.connection.is_connected():
            logging.error("No connection to the database.")
            return
        return func(self, *args, **kwargs)
    return wrapper

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
                logging.info("Connected to MySQL database")
        except Error as e:
            logging.error(f"Error while connecting to MySQL: {e}")

    @ensure_connection
    def create_tables(self):
        try:
            with self.connection.cursor() as cursor:
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
            logging.info("Tables created successfully")
        except Error as e:
            logging.error(f"Error while creating tables: {e}")

    @ensure_connection
    def populate_from_json(self, json_file_path):
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                region_data = json.load(file)

            with self.connection.cursor() as cursor:
                self._insert_countries_and_regions(cursor, region_data)

            self.connection.commit()
            logging.info("Data inserted successfully into countries, regions, and subregions tables")
        except Error as e:
            logging.error(f"Error while populating tables: {e}")

    def _insert_countries_and_regions(self, cursor, region_data):
        for country, regions in region_data.items():
            cursor.execute("INSERT INTO countries (country_name) VALUES (%s)", (country,))
            country_id = cursor.lastrowid
            logging.info(f"Inserted country: {country} with ID: {country_id}")
            self._insert_regions(cursor, country_id, regions)

    def _insert_regions(self, cursor, country_id, regions):
        for region, subregions in regions.items():
            cursor.execute("INSERT INTO regions (region_name, country_id, parent_region_id) VALUES (%s, %s, NULL)", (region, country_id))
            region_id = cursor.lastrowid
            logging.info(f"Inserted region: {region} with ID: {region_id}")
            self._insert_subregions(cursor, country_id, region_id, subregions)

    def _insert_subregions(self, cursor, country_id, region_id, subregions):
        if isinstance(subregions, dict):
            for subregion, microregions in subregions.items():
                cursor.execute("INSERT INTO regions (region_name, country_id, parent_region_id) VALUES (%s, %s, %s)", (subregion, country_id, region_id))
                subregion_id = cursor.lastrowid
                logging.info(f"Inserted subregion: {subregion} under region ID: {region_id}")
                self._insert_microregions(cursor, country_id, subregion_id, microregions)
        elif isinstance(subregions, list):
            for subregion in subregions:
                cursor.execute("INSERT INTO regions (region_name, country_id, parent_region_id) VALUES (%s, %s, %s)", (subregion, country_id, region_id))
                logging.info(f"Inserted subregion: {subregion} under region ID: {region_id}")

    def _insert_microregions(self, cursor, country_id, subregion_id, microregions):
        for microregion in microregions:
            cursor.execute("INSERT INTO regions (region_name, country_id, parent_region_id) VALUES (%s, %s, %s)", (microregion, country_id, subregion_id))
            logging.info(f"Inserted microregion: {microregion} under subregion ID: {subregion_id}")

    @ensure_connection
    def get_all_wines(self):
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT w.name, t.type_name, w.year, r.region_name, w.price, w.quantity 
                    FROM wines w
                    JOIN types t ON w.type_id = t.id
                    JOIN regions r ON w.region_id = r.id
                """)
                wines = cursor.fetchall()
            return wines
        except Error as e:
            logging.error(f"Error fetching wines: {e}")
            return []
        
    @ensure_connection
    def get_id_from_name(self, table, name):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM {table} WHERE {table[:-1]}_name = %s", (name,))
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            logging.error(f"Error fetching ID from {table}: {e}")
            return None

    @ensure_connection
    def get_types(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT type_name FROM types")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logging.error(f"Error fetching wine types: {e}")
            return []

    @ensure_connection
    def get_regions(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT region_name FROM regions")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logging.error(f"Error fetching wine regions: {e}")
            return []
              
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("MySQL connection is closed")

# Example of using the Database class to create tables and populate from JSON
if __name__ == "__main__":
    db = Database()
    db.create_tables()
    db.populate_from_json('webScraper/wine_regions.json')
    db.close_connection()
