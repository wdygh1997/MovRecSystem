import tkinter as tk
import threading as th
import dbcon.mysqlcon
import gui.home
import gui.movieframe
import gui.navbar

Images = []


class User:
    def __init__(self, window, frame, user_id, movie_id):
        self.window = window
        self.frame = frame
        self.user_id = user_id

        bar_frame = tk.Frame(self.frame, width=800, height=20)
        bar_frame.pack_propagate(False)
        bar_frame.place(x=0, y=0, anchor="nw")
        gui.navbar.NavBar(self.window, self.frame, bar_frame, self.user_id, movie_id, page="U")

        con, cur = dbcon.mysqlcon.mysql_connect()
        cur.execute("select movieId, rating, timestamp from movrecsystem.ratings where userId={}  order by timestamp desc limit 15;".format(self.user_id))
        result = cur.fetchall()
        cur.execute("select count(rating) from movrecsystem.ratings where userId={};".format(self.user_id))
        num = cur.fetchall()[0][0]
        dbcon.mysqlcon.mysql_close(con, cur)

        tk.Label(self.frame, text="您已经给{}部电影打过分,仅向您展示最近15部电影！".format(num)).place(x=0, y=20, anchor='nw')

        if num == 0:
            tk.Label(self.frame, text="您还没有给电影评过分！", font=('', 20)).place(x=250, y=156, anchor="nw")
        if num > 0:
            self.list1_frame = tk.Frame(self.frame)
            self.list1_frame.place(x=15, y=50)
            movie_list1 = result[:5]
            print(movie_list1)
            for tup in movie_list1:
                t = th.Thread(target=self.job, args=(self.list1_frame, tup[0], tup[1], tup[2]))
                t.start()

        if num > 5:
            self.list2_frame = tk.Frame(self.frame)
            self.list2_frame.place(x=15, y=250)
            movie_list2 = result[5:10]
            print(movie_list2)
            for tup in movie_list2:
                t = th.Thread(target=self.job, args=(self.list2_frame, tup[0], tup[1], tup[2]))
                t.start()

        if num > 10:
            self.list3_frame = tk.Frame(self.frame)
            self.list3_frame.place(x=15, y=450)
            movie_list3 = result[10:15]
            print(movie_list3)
            for tup in movie_list3:
                t = th.Thread(target=self.job, args=(self.list3_frame, tup[0], tup[1], tup[2]))
                t.start()

    def job(self, frame, movie_id, rating, time):
        temp = gui.movieframe.MovieFrame(self.window, self.frame, frame, self.user_id, movie_id, page="U", time=time, rating=rating)
        Images.append(temp.photo_image)
        temp.info_frame.pack(side='left')
