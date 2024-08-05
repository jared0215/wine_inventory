# init_db.py

from src.models import Database

def initialize_database():
    db = Database()
    db.create_tables()

    populate_initial_data(db)

    db.close_connection()

def populate_initial_data(db):
    cursor = db.connection.cursor()

    # Populate the types table if empty
    cursor.execute("SELECT COUNT(*) FROM types")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO types (type_name) VALUES (%s)", [('Red',), ('White',), ('Rosé',), ('Sparkling',)])
        db.connection.commit()
        print("Types table populated with initial data.")

    # Populate the regions table if empty
    cursor.execute("SELECT COUNT(*) FROM regions")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO regions (region_name) VALUES (%s)", [('Napa Valley',), ('Bordeaux',), ('Tuscany',), ('Barossa Valley',)])
        db.connection.commit()
        print("Regions table populated with initial data.")

    cursor.close()

if __name__ == "__main__":
    initialize_database()
