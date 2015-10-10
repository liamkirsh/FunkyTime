import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('local.db')
        
        if not self.db_exists():
            self.create_db()

    def db_exists(self):
        return False

    def create_db(self):
        return False
