import sqlite3
from sqlite3.dbapi2 import Error

#create connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

#create table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

#create ticket
def create_ticket(conn, ticket):

    sql = "INSERT INTO ticket(member_id,channel_id) VALUES(?,?)"
    cur = conn.cursor()
    cur.execute(sql, ticket)
    conn.commit()
    return cur.lastrowid

#query ticket for channel id
def query_tickit_id(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ticket WHERE channel_id=?", (id,))
    rows = cur.fetchall()
    return rows

#query ticket for member id
def query_tickit_uid(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ticket WHERE member_id=?", (id,))
    rows = cur.fetchall()
    return rows

#delete ticket

def delete_ticket(conn, id):
    cur = conn.cursor()
    cur.execute("DELETE FROM ticket WHERE channel_id=?", (id,))
    conn.commit()


#create apply
def create_apply(conn, id):

    cur = conn.cursor()
    cur.execute("INSERT INTO apply(message_id) VALUES(?)", (id,))
    conn.commit()
    return cur.lastrowid

#query apply
def query_apply(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM apply")
    rows = cur.fetchall()
    return rows

#delete apply

def delete_apply(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM apply")
    conn.commit()