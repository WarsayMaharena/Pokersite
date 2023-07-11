import sqlite3 
from sqlite3 import Error



class User:
    def __init__(self):
        conn = None 
        try:
            self.conn = sqlite3.connect(r"poker_database.db")
        except Error as e:
            print(e)

    def add_user(self, user_name, password, email, currency=0):
        cur = self.conn.cursor()
        sql_insert = """INSERT INTO Users VALUES (%s, %s, %s, %s);"""
        val = (user_name, password, email, currency)
        cur.execute(sql_insert, val)
        self.conn.commit()
        self.conn.close()

    def delete_user(self, user_name, password, email):
        cur = self.conn.cursor()
        sql_delete = """DELETE FROM Users WHERE user_name=%s"""
        val = user_name
        cur.execute(sql_delete, val)
        self.conn.commit()
        self.conn.close()

    def update_password(self, user_name, email, password):
        pass

    def login(self, user_name, password):
        pass

    
    