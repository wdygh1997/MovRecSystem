import dbcon.mysqlcon

con, cur = dbcon.mysqlcon.mysql_connect()

# 创建数据库movrecsystem
cur.execute("DROP DATABASE IF EXISTS movrecsystem;")
cur.execute("CREATE DATABASE movrecsystem;")

dbcon.mysqlcon.mysql_close(con, cur)
