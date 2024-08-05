# init_db.py

from src.models import Database

def initialize_database():
    db = Database()
    db.create_tables()

    db.close_connection()


if __name__ == "__main__":
    initialize_database()
