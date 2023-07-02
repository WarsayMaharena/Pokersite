import mysql.connector



class User():
    def __init__(self):
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="rootpass",
        auth_plugin='mysql_native_password',
        database="Testing")

        self.mycursor = self.db.cursor()
