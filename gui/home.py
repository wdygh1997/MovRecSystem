import tkinter as tk
import threading as th
import dbcon.mysqlcon
import gui.user
import gui.movieframe
import gui.navbar
import gui.method

Images = []


class Home:
    def __init__(self, window, frame, user_id, movie_id):
        self.window = window
        self.frame = frame
        self.user_id = user_id
        self.movie_id = movie_id

        bar_frame = tk.Frame(self.frame, width=800, height=20)
        bar_frame.pack_propagate(False)
        bar_frame.place(x=0, y=0, anchor="nw")
        gui.navbar.NavBar(self.window, self.frame, bar_frame, self.user_id, self.movie_id, page="H")

        if user_id is None:
            tk.Label(self.frame, text="您还未登录！\n点击右上角按钮登录！", font=('', 20)).place(x=230, y=130, anchor='nw')
            tk.Label(self.frame, text="<向您推荐热门电影>").place(x=15, y=300, anchor='nw')
            self.hot_movie_frame = tk.Frame(self.frame)
            self.hot_movie_frame.place(x=15, y=340, anchor='nw')
            self.hot_movie()
        else:
            tk.Label(self.frame, text="<向您提供离线推荐(基于SVD分解)>").place(x=15, y=15, anchor='nw')
            self.offline_svd_frame = tk.Frame(self.frame)
            self.offline_svd_frame.place(x=15, y=35, anchor='nw')
            self.offline_svd()

            tk.Label(self.frame, text="<向您提供离线推荐(基于NMF分解)>").place(x=15, y=172, anchor='nw')
            self.offline_nmf_frame = tk.Frame(self.frame)
            self.offline_nmf_frame.place(x=15, y=192, anchor='nw')
            self.offline_nmf()

            tk.Label(self.frame, text="<向您提供在线推荐(基于SVD分解)>").place(x=15, y=329, anchor='nw')
            self.online_svd_frame = tk.Frame(self.frame)
            self.online_svd_frame.place(x=15, y=349, anchor='nw')
            self.online_svd()

            tk.Label(self.frame, text="<向您提供在线推荐(基于NMF分解)>").place(x=15, y=486, anchor='nw')
            self.online_nmf_frame = tk.Frame(self.frame)
            self.online_nmf_frame.place(x=15, y=506, anchor='nw')
            self.online_nmf()

    def hot_movie(self):
        con, cur = dbcon.mysqlcon.mysql_connect()
        cur.execute("select movieId, count(1) from movrecsystem.ratings group by movieId order by count(1) desc limit 5;")
        result = cur.fetchall()
        dbcon.mysqlcon.mysql_close(con, cur)
        print(result)
        for tup in result:
            t = th.Thread(target=self.job, args=(self.hot_movie_frame, tup[0]))
            t.start()

    def offline_svd(self):
        con, cur = dbcon.mysqlcon.mysql_connect()
        cur.execute("select recId from movrecsystem.pdtsvd where userid={} order by pdtScore desc limit 5;".format(self.user_id))
        result = cur.fetchall()
        dbcon.mysqlcon.mysql_close(con, cur)
        print(result)
        if len(result) > 0:
            for tup in result:
                t = th.Thread(target=self.job, args=(self.offline_svd_frame, tup[0]))
                t.start()
        else:
            tk.Label(self.offline_svd_frame, text="您是最近新用户，系统尚未录入离线推荐信息!", font=('', 15)).pack(side='bottom')

    def offline_nmf(self):
        con, cur = dbcon.mysqlcon.mysql_connect()
        cur.execute("select recId from movrecsystem.pdtnmf where userid={} order by pdtScore desc limit 5;".format(self.user_id))
        result = cur.fetchall()
        dbcon.mysqlcon.mysql_close(con, cur)
        print(result)
        if len(result) > 0:
            for tup in result:
                t = th.Thread(target=self.job, args=(self.offline_nmf_frame, tup[0]))
                t.start()
        else:
            tk.Label(self.offline_nmf_frame, text="您是最近新用户，系统尚未录入离线推荐信息!", font=('', 15)).pack(side='bottom')

    def online_svd(self):
        page = "new"
        if self.user_id <= 610:
            page = "old"
        con, cur = dbcon.mysqlcon.mysql_connect()
        cur.execute("select movieId, timestamp from movrecsystem.ratings where userId={}  order by timestamp desc limit 1;".format(self.user_id))
        mov_id = cur.fetchall()
        dbcon.mysqlcon.mysql_close(con, cur)
        if len(mov_id) > 0:
            mov_id = mov_id[0][0]
            result = gui.method.get_online_svd(self.user_id, mov_id, page)
            print(result)
            for tup in result:
                t = th.Thread(target=self.job, args=(self.online_svd_frame, tup))
                t.start()
        else:
            tk.Label(self.online_svd_frame, text="您还未给任何电影评分，无法向您提供在线推荐!", font=('', 15)).pack(side='bottom')

    def online_nmf(self):
        page = "new"
        if self.user_id <= 610:
            page = "old"
        con, cur = dbcon.mysqlcon.mysql_connect()
        cur.execute("select movieId, timestamp from movrecsystem.ratings where userId={}  order by timestamp desc limit 1;".format(self.user_id))
        mov_id = cur.fetchall()
        dbcon.mysqlcon.mysql_close(con, cur)
        if len(mov_id) > 0:
            mov_id = mov_id[0][0]
            result = gui.method.get_online_nmf(self.user_id, mov_id, page)
            print(result)
            for tup in result:
                t = th.Thread(target=self.job, args=(self.online_nmf_frame, tup))
                t.start()
        else:
            tk.Label(self.online_nmf_frame, text="您还未给任何电影评分，无法向您提供在线推荐!", font=('', 15)).pack(side='bottom')

    def job(self, frame, movie_id):
        temp = gui.movieframe.MovieFrame(self.window, self.frame, frame, self.user_id, movie_id)
        Images.append(temp.photo_image)
        temp.info_frame.pack(side='left')
