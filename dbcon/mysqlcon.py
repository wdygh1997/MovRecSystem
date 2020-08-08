import mysql.connector


def mysql_connect():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456"
    )
    cur = con.cursor()
    return con, cur


def mysql_close(con, cur):
    cur.close()
    con.close()
