# init_db.py

from src.models import Database

db = Database()
db.create_tables()

def populate_initial_data():
    cursor = db.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM types")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO types (type_name) VALUES (%s)", [('Red',), ('White',), ('Rosé',), ('Sparkling',)])
        db.connection.commit()

    cursor.execute("SELECT COUNT(*) FROM regions")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO regions (region_name) VALUES (%s)", [('Napa Valley',), ('Bordeaux',), ('Tuscany',), ('Barossa Valley',)])
        db.connection.commit()

populate_initial_data()
db.close_connection()
