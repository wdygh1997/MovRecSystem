import dbcon.mysqlcon
import loaddata.path

con, cur = dbcon.mysqlcon.mysql_connect()

cur.execute("USE movrecsystem;")

# 创建links数据表并加载数据links.csv
cur.execute("DROP TABLE IF EXISTS links;")
cur.execute("CREATE TABLE links (movieId int, imdbId int);")
cur.execute('''LOAD DATA INFILE '{}' INTO TABLE links
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\r\n'
            IGNORE 1 LINES;'''.format(loaddata.path.links_path))
con.commit()

# 创建movies数据表并加载数据movies.csv
cur.execute("DROP TABLE IF EXISTS movies;")
cur.execute("CREATE TABLE movies (movieId int, title varchar(200), genres varchar(100));")
cur.execute('''LOAD DATA INFILE '{}' INTO TABLE movies
            FIELDS TERMINATED BY ','
            OPTIONALLY ENCLOSED BY '"'
            LINES TERMINATED BY '\r\n'
            IGNORE 1 LINES;'''.format(loaddata.path.movies_path))
con.commit()

# 创建ratings数据表并加载数据ratings.csv
cur.execute("DROP TABLE IF EXISTS ratings;")
cur.execute("CREATE TABLE ratings (userId int, movieId int, rating float, timestamp int);")
cur.execute('''LOAD DATA INFILE '{}' INTO TABLE ratings
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\r\n'
            IGNORE 1 LINES;'''.format(loaddata.path.ratings_path))
con.commit()

# 创建tags数据表并加载数据tags.csv
cur.execute("DROP TABLE IF EXISTS tags;")
cur.execute("CREATE TABLE tags (userId int, movieId int, tag varchar(100), timestamp int);")
cur.execute('''LOAD DATA INFILE '{}' INTO TABLE tags
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\r\n'
            IGNORE 1 LINES;'''.format(loaddata.path.tags_path))
con.commit()

# 创建users数据表并插入数据，users数据表存储用户名和密码，密码与用户名相同，MovieLens数据集初始只有610个用户
cur.execute("DROP TABLE IF EXISTS users;")
cur.execute("CREATE TABLE users (userId int, pwd varchar(50));")
for i in range(1, 611):
    cur.execute("insert into movrecsystem.users values({},{})".format(i, i))
con.commit()

dbcon.mysqlcon.mysql_close(con, cur)
