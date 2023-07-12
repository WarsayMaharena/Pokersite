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
        sql_insert = "INSERT INTO Users VALUES(?,?,?,?,?)"
        id = self.calc_userid()
        val = (id, user_name, password, email, currency)
        cur.execute(sql_insert, val)
        self.conn.commit()
        self.conn.close()

    def delete_user(self, user_name, password, email):
        cur = self.conn.cursor()
        sql_delete = "DELETE FROM Users WHERE user_name=?"
        val = (user_name)
        cur.execute(sql_delete, (user_name,))
        self.conn.commit()
        self.conn.close()

    def calc_userid(self):
        cur = self.conn.cursor()
        sql_select = "SELECT id FROM Users"
        cur.execute(sql_select)
        result = cur.fetchall()
        if result != None:
            id = len(result) + 1
            print(id)
            return id
        else:
            print(1)
            return 1

    #Method used when creating a new account to see if there is no current email or username already in use
    def check_new_user(self, user_name, email):
        cur = self.conn.cursor()
        sql_select = "SELECT * FROM Users WHERE user_name=? OR email=?"
        val = (user_name, email)
        cur.execute(sql_select, val)
        result = cur.fetchone()
        if result == None:
            print("Couldnt find account with that username or email")
            return True
        else:
            print("There already exists an account with that name")
            return False
        

    def update_password(self, user_name, email, password):
        pass

    #Method used when logging in to check if username and password exists in database
    def authentication(self, user_name, password):
        cur = self.conn.cursor()
        sql_select = "SELECT * FROM Users WHERE user_name=? AND password=?"
        val = (user_name, password)
        cur.execute(sql_select, val)
        result = cur.fetchone()
        if result == None:
            print("Authentication failed")
            return False 
        else:
            print("Authentication successful")
            self.conn.close()
            return True
       
            

#user = User()
#user.add_user('klasse', 'spegel666', 'spegelman@ħotmail.com')
#user.delete_user('klas', 'aqwrj2', 'klasaman99@hotmail.com')
#user.authentication('klas', 'aqwrj2')
#user.check_new_user(user_name="kalas", email="klasamaan99@ħotmail.com")
#user.calc_userid()