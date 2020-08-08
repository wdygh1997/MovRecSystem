import dbcon.mysqlcon
import loaddata.path

con, cur = dbcon.mysqlcon.mysql_connect()

cur.execute("USE movrecsystem;")

# 创建simsvd数据表并加载数据simSVD.csv
cur.execute("DROP TABLE IF EXISTS simsvd;")
cur.execute("CREATE TABLE simsvd (movieId int, simId int, simDegree float);")
cur.execute('''LOAD DATA INFILE '{}' INTO TABLE simsvd
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\r\n'
            IGNORE 1 LINES;'''.format(loaddata.path.simSVD_path))
con.commit()

# 创建pdtsvd数据表并加载数据pdtSVD.csv
cur.execute("DROP TABLE IF EXISTS pdtsvd;")
cur.execute("CREATE TABLE pdtsvd (userId int, recId int, pdtScore float);")
cur.execute('''LOAD DATA INFILE '{}' INTO TABLE pdtsvd
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\r\n'
            IGNORE 1 LINES;'''.format(loaddata.path.pdtSVD_path))
con.commit()

# 创建simnmf数据表并加载数据simNMF.csv
cur.execute("DROP TABLE IF EXISTS simnmf;")
cur.execute("CREATE TABLE simnmf (movieId int, simId int, simDegree float);")
cur.execute('''LOAD DATA INFILE '{}' INTO TABLE simnmf
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\r\n'
            IGNORE 1 LINES;'''.format(loaddata.path.simNMF_path))
con.commit()

# 创建pdtnmf数据表并加载数据pdtNMF.csv
cur.execute("DROP TABLE IF EXISTS pdtnmf;")
cur.execute("CREATE TABLE pdtnmf (userId int, recId int, pdtScore float);")
cur.execute('''LOAD DATA INFILE '{}' INTO TABLE pdtnmf
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\r\n'
            IGNORE 1 LINES;'''.format(loaddata.path.pdtNMF_path))
con.commit()

# 创建simol数据表并加载数据simOL.csv
cur.execute("DROP TABLE IF EXISTS simol;")
cur.execute("CREATE TABLE simol (movieId int, simId int);")
cur.execute('''LOAD DATA INFILE '{}' INTO TABLE simol
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\r\n'
            IGNORE 1 LINES;'''.format(loaddata.path.simOL_path))
con.commit()

# 创建pdtol数据表并加载数据pdtOL.csv
cur.execute("DROP TABLE IF EXISTS pdtol;")
cur.execute("CREATE TABLE pdtol (userId int, recId int);")
cur.execute('''LOAD DATA INFILE '{}' INTO TABLE pdtol
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\r\n'
            IGNORE 1 LINES;'''.format(loaddata.path.pdtOL_path))
con.commit()

dbcon.mysqlcon.mysql_close(con, cur)
