import tkinter as tk
import threading as th
import dbcon.mysqlcon
import gui.home
import gui.movieframe
import gui.navbar

Images = []


class Search:
    def __init__(self, window, frame, user_id, movie_id):
        self.window = window
        self.frame = frame
        self.user_id = user_id

        bar_frame = tk.Frame(self.frame, width=800, height=20)
        bar_frame.pack_propagate(False)
        bar_frame.place(x=0, y=0, anchor="nw")
        gui.navbar.NavBar(self.window, self.frame, bar_frame, self.user_id, movie_id, page="S")

        self.search_txt = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.search_txt).place(x=58, y=48, anchor='nw')
        tk.Button(self.frame, text="搜索", command=self.get_search).place(x=249, y=46)

        self.result_Frame = tk.Frame(self.frame, width=800, height=700)
        self.result_Frame.pack_propagate(False)
        self.result_Frame.place(x=0, y=90, anchor='nw')

    def get_search(self):
        self.result_Frame.destroy()
        self.result_Frame = tk.Frame(self.frame, width=800, height=700)
        self.result_Frame.pack_propagate(False)
        self.result_Frame.place(x=0, y=90, anchor='nw')

        search_txt = self.search_txt.get()

        con, cur = dbcon.mysqlcon.mysql_connect()
        sql = "select movieId from movrecsystem.movies where title like '%{}%';".format(search_txt)
        cur.execute(sql)
        data = cur.fetchall()
        dbcon.mysqlcon.mysql_close(con, cur)

        tk.Label(self.result_Frame, text="系统为您搜索到{}部电影,仅向您展示15部电影！".format(len(data))).place(x=58, y=0, anchor='nw')

        if len(data) == 0:
            tk.Label(self.result_Frame, text="没有搜索到相关的电影！", font=('', 20)).place(x=250, y=60, anchor="nw")
        if len(data) > 0:
            list1_frame = tk.Frame(self.result_Frame)
            list1_frame.place(x=15, y=50)
            movie_list1 = data[:5]
            print(movie_list1)
            for tup in movie_list1:
                t = th.Thread(target=self.job, args=(list1_frame, tup[0]))
                t.start()

        if len(data) > 5:
            list2_frame = tk.Frame(self.result_Frame)
            list2_frame.place(x=15, y=230)
            movie_list2 = data[5:10]
            print(movie_list2)
            for tup in movie_list2:
                t = th.Thread(target=self.job, args=(list2_frame, tup[0]))
                t.start()

        if len(data) > 10:
            list3_frame = tk.Frame(self.result_Frame)
            list3_frame.place(x=15, y=410)
            movie_list3 = data[10:15]
            print(movie_list3)
            for tup in movie_list3:
                t = th.Thread(target=self.job, args=(list3_frame, tup[0]))
                t.start()

    def job(self, frame, movie_id):
        temp = gui.movieframe.MovieFrame(self.window, self.frame, frame, self.user_id, movie_id)
        Images.append(temp.photo_image)
        temp.info_frame.pack(side='left')
