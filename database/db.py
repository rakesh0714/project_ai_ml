import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


class Database:

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"]
            )

            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("✅ Connected to MySQL Database")

        except Error as e:
            print("Database Connection Error:", e)

    # ----------------------------
    # INSERT
    # ----------------------------

    def insert(self, query, values):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            print(e)
            return False

    # ----------------------------
    # SELECT
    # ----------------------------

    def fetch_all(self, query, values=None):
        self.cursor.execute(query, values or ())
        return self.cursor.fetchall()

    def fetch_one(self, query, values=None):
        self.cursor.execute(query, values or ())
        return self.cursor.fetchone()

    # ----------------------------
    # UPDATE
    # ----------------------------

    def update(self, query, values):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            print(e)
            return False

    # ----------------------------
    # DELETE
    # ----------------------------

    def delete(self, query, values):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            print(e)
            return False

    # ----------------------------
    # CLOSE CONNECTION
    # ----------------------------

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()


db = Database()