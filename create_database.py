import sqlite3
from sqlite3 import Error
import random
from string import ascii_uppercase



# Creates a connection to database file, if database file does not exist it creates a new database file
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print("Created connection")
    except Error as e:
        print(e)

    return conn


def create_tables():
    database = r"poker_database.db"

    sql_user_table = """CREATE TABLE IF NOT EXISTS Users (
                            id Integer PRIMARY KEY,
                            user_name text,
                            password text,
                            email text,
                            funds Integer
                            );"""
    
    sql_room_table = """CREATE TABLE IF NOT EXISTS Rooms (
                            roomid text PRIMARY KEY,
                            members integer
                            );"""
    
    sql_comment_table = """CREATE TABLE IF NOT EXISTS Comments (
                            commentid Integer PRIMARY KEY,
                            roomid integer,
                            user_name text,
                            message text
                            );"""
    

    sql_card_table = """CREATE TABLE IF NOT EXISTS Cards (
                        card_number Integer PRIMARY KEY,
                        cvc Integer,
                        expiration_date Integer,
                        user_name text,
                        FOREIGN KEY (user_name) REFERENCES Users (user_name)
    );
    """

    conn = create_connection(database)
    c = conn.cursor()
    
    if conn is not None:
        c.execute(sql_user_table)
        c.execute(sql_card_table)
        c.execute(sql_comment_table)
        c.execute(sql_room_table)
    c.close()


def show_users_table():
    database = r"poker_database.db"

    conn = create_connection(database)
    c = conn.cursor()
    sql_select_query = """SELECT * FROM Comments
    ;
    """
    c.execute(sql_select_query)
    print(c.fetchall())
    c.close()


def show_cards_table():
    database = r"poker_database.db"

    conn = create_connection(database)
    c = conn.cursor()
    sql_select_query = """SELECT * FROM Cards
    );
    """
    c.execute(sql_select_query)
    c.close()

def show_tabels():
    database = r"poker_database.db"

    conn = create_connection(database)
    c = conn.cursor()
    sql_select_query = """SELECT name FROM sqlite_master  
  WHERE type='table'
    """
    c.execute(sql_select_query)
    print(c.fetchall())
    c.close()    
    



def test_insert():
    database = r"poker_database.db"
    conn = create_connection(database)
    c = conn.cursor()

    sql_insert_query = """INSERT INTO Rooms VALUES ('AJYZ', 8);"""

    c.execute(sql_insert_query)
    conn.commit()
    c.close()
    
class User():
    ############## SQL insert, retrieve eller delete Kommando ##########################################
    def __init__(self):
        database = r"poker_database.db"
        self.conn = create_connection(database)
        self.c = self.conn.cursor()

    def insert_comment(self, name, roomid, message):
        database = r"poker_database.db"
        conn = create_connection(database)
        c = conn.cursor()
        commentid_val=self.calc_new_commentid()
        sql_insert_query = """INSERT INTO Comments VALUES (%s, '%s', '%s', '%s');"""%(commentid_val,roomid,name,message)
        c.execute(sql_insert_query)
        conn.commit()
        
        

    def calc_new_commentid(self):
        database = r"poker_database.db"
        conn = create_connection(database)
        c = conn.cursor()
        sql3 = "SELECT MAX(commentid) FROM Comments"
        c.execute(sql3)
        myresult = c.fetchall()[0][0]
        print("MAX: ",myresult)
        if myresult == None:
            return 1
        else:
            customerid = myresult + 1
            return customerid
        
    def room_exists(self, room): #checks if the user is trying to join actually exists
        database = r"poker_database.db"
        conn = create_connection(database)
        c = conn.cursor()
        sql3="""SELECT roomid FROM Rooms WHERE roomid='%s';"""%(room)
        c.execute(sql3)
        myresult=c.fetchall()
        if len(myresult) == 0:
            c.close()
            return False
        else:
            return True
        
    def member_exists(self,room):
        database = r"poker_database.db"
        conn = create_connection(database)
        c = conn.cursor()
        sql3="""SELECT members FROM Rooms WHERE roomid='%s';"""%(room)
        c.execute(sql3)
        myresult=c.fetchall()
        if myresult[0][0] == 0:
            c.close()
            print("false")
            return False
        else:
            return True
               
        
    def add_member(self, room): #adds a member to the room
        database = r"poker_database.db"
        conn = create_connection(database)
        c = conn.cursor()
        sql3="""SELECT members FROM Rooms WHERE roomid='%s';"""%(room)
        c.execute(sql3)
        myresult=c.fetchall()
        if(len(myresult)!=0):
            AddedMember=myresult[0][0]+1
        print(AddedMember," ", room)
        sql3_1="""UPDATE Rooms SET members = %s WHERE roomid = '%s';"""%(AddedMember,room)
        c.execute(sql3_1)
        conn.commit()

    def sub_member(self, room):
        database = r"poker_database.db"
        conn = create_connection(database)
        c = conn.cursor()
        sql3="""SELECT members FROM Rooms WHERE roomid='%s';"""%(room)
        c.execute(sql3)
        myresult=c.fetchall()
        if(len(myresult)!=0):
            SubbedMember=myresult[0][0]-1
        print(SubbedMember," ", room)
        sql3_1="""UPDATE Rooms SET members = %s WHERE roomid = '%s';"""%(SubbedMember,room)
        c.execute(sql3_1)
        conn.commit()
   
    def del_room(self, room): #deletes the room once all members have left
        database = r"poker_database.db"
        conn = create_connection(database)
        c = conn.cursor()
        sql3 = """DELETE FROM Rooms WHERE roomid='%s';"""%(room)
        c.execute(sql3)
        conn.commit()
        c.close

    def show_rooms(self):
        sql3 = "SELECT * FROM Rooms"
        self.c.execute(sql3)
        myresult=self.c.fetchall()
        return myresult
    
    def generate_unique_code(self):
        database = r"poker_database.db"
        conn = create_connection(database)
        c = conn.cursor()
        code = "" #genererar en kod för rummet
        for _ in range(6): 
            code += random.choice(ascii_uppercase)
        sql3="""SELECT roomid FROM Rooms WHERE roomid='%s';"""%(code)
        c.execute(sql3)
        myresult=c.fetchall()
        while True:
            if len(myresult) == 0:
                    sql_insert_query = """INSERT INTO Rooms VALUES ('%s', %s);"""%(code,0)
                    c.execute(sql_insert_query)
                    conn.commit()
                    c.close()
                    print("here1")
                    break   
            
            else: #om koden redan existerar generas en ny kod för rummet
                print("#######LOOP1######## \nold code: ",code,"\n")
                code=""
                for _ in range(6):
                    code += random.choice(ascii_uppercase)
                print("new code: ", code,"\n\n")
        
        return code
    
    ############## Hjälp funktioner för SQL kommando ##########################################











 

create_connection(r"poker_database.db")
create_tables()
#user=User()

#test_insert()
user=User()
user.insert_comment("hello", 'there', "kenobi")
#user.member_exists("XRYDNQ")
#user.room_exists('AJYZ')
#user.show_rooms()
#show_tabels()
print(type(show_users_table()))
#user.add_member('MNMCIM')
#function()
#print(user.generate_unique_code())
#print(user.show_rooms())