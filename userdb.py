import mysql.connector


class User():
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost", user="root", passwd="rootpass", auth_plugin='mysql_native_password', database="Pokerdb")
        self.mycursor = self.db.cursor()



user=User()
user.mycursor.execute("show databases;")

for i in user.mycursor:
    print(i)
