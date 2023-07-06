import sqlite3
from sqlite3 import Error



# Creates a connection to database file, if database file does not exist it creates a new database file
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Created connection")
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
    c.close()


def show_users_table():
    database = r"poker_database.db"

    conn = create_connection(database)
    c = conn.cursor()
    sql_select_query = """SELECT * FROM Users
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



def test_insert():
    database = r"poker_database.db"
    conn = create_connection(database)
    c = conn.cursor()

    sql_insert_query = """INSERT INTO Users VALUES (1, 'klas', 'aqwrj2', 'klasaman99@hotmail.com', 70);
    """
    
    c.execute(sql_insert_query)
    conn.commit()
    c.close()


#create_connection(r"poker_database.db")
#create_tables()

show_users_table()