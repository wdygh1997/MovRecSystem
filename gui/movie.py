import tkinter as tk
import tkinter.messagebox
import threading as th
import time
import dbcon.mysqlcon
import gui.movieframe
import gui.navbar
import gui.method

Images = []


class Movie:
    def __init__(self, window, frame, user_id, movie_id):
        self.window = window
        self.frame = frame
        self.user_id = user_id
        self.movie_id = movie_id

        bar_frame = tk.Frame(self.frame, width=800, height=20)
        bar_frame.pack_propagate(False)
        bar_frame.place(x=0, y=0, anchor="nw")
        gui.navbar.NavBar(self.window, self.frame, bar_frame, self.user_id, self.movie_id, page="M")

        north_frame = tk.Frame(self.frame, width=800, height=250)
        north_frame.place(x=0, y=20)
        url = gui.method.get_url(self.movie_id)
        src, title, date, genres = gui.method.get_src(url, self.movie_id)

        left_frame = tk.Frame(north_frame, width=200, height=250)
        left_frame.place(x=0, y=0, anchor="nw")

        photo_image = gui.method.get_image(src, w_box=120, h_box=200)
        Images.append(photo_image)
        tk.Label(left_frame, image=photo_image).place(x=45, y=20, anchor="nw")

        right_frame = tk.Frame(north_frame, height=250, width=600)
        right_frame.place(x=200, y=0, anchor="nw")
        tk.Label(right_frame, text="标题:{}".format(title), font=("", 15), height=1).place(x=0, y=15)
        tk.Label(right_frame, text="时间:{}".format(date), font=("", 15), height=1).place(x=0, y=50)
        genres = genres.strip('""').replace(",", "").replace('"', "").replace(" ", '')
        tk.Label(right_frame, text="类型:\n" + genres, font=("", 15)).place(x=0, y=80)

        if self.user_id is not None:
            tk.Button(right_frame, text="评分", command=self.rate).place(x=460, y=160)

        tk.Label(self.frame, text="<向您推荐相似电影(基于SVD分解)>").place(x=25, y=280, anchor="nw")
        con, cur = dbcon.mysqlcon.mysql_connect()
        cur.execute("select simId, simDegree from movrecsystem.simsvd where movieId={} order by simDegree desc limit 5;".format(self.movie_id))
        result_svd = cur.fetchall()
        dbcon.mysqlcon.mysql_close(con, cur)
        print(result_svd)
        svd_frame = tk.Frame(self.frame)
        svd_frame.place(x=15, y=300, anchor="nw")
        for tup in result_svd:
            t = th.Thread(target=self.job, args=(tup[0], tup[1], svd_frame))
            t.start()

        tk.Label(self.frame, text="<向您推荐相似电影(基于NMF分解)>").place(x=25, y=460, anchor="nw")
        con, cur = dbcon.mysqlcon.mysql_connect()
        cur.execute("select simId, simDegree from movrecsystem.simnmf where movieId={} order by simDegree desc limit 5;".format(self.movie_id))
        result_nmf = cur.fetchall()
        dbcon.mysqlcon.mysql_close(con, cur)
        print(result_nmf)
        nmf_frame = tk.Frame(self.frame)
        nmf_frame.place(x=15, y=480, anchor="nw")
        for tup in result_nmf:
            t = th.Thread(target=self.job, args=(tup[0], tup[1], nmf_frame))
            t.start()

    def rate(self):
        print("rate按钮被点击...")
        con, cur = dbcon.mysqlcon.mysql_connect()
        cur.execute("select rating, timestamp from movrecsystem.ratings where movieId={} and userId={};".format(self.movie_id, self.user_id))
        result = cur.fetchall()
        dbcon.mysqlcon.mysql_close(con, cur)

        if len(result) == 0:
            UnratedFrame(self.window, self.user_id, self.movie_id, "insert")
        else:
            rating, rated_time = result[0][0], result[0][1]
            RatedFrame(self.window, self.user_id, self.movie_id, rating, rated_time)

    def job(self, movie_id, sim_degree, frame):
        temp = gui.movieframe.MovieFrame(self.window, self.frame, frame, self.user_id, movie_id, page="M", simDegree=sim_degree)
        Images.append(temp.photo_image)
        temp.info_frame.pack(side='left')


# page值：edit表示此时是在修改电影评分，insert表示此时是在新增电影评分
class UnratedFrame:
    def __init__(self, window, user_id, movie_id, page):
        self.window = window
        self.user_id = user_id
        self.movie_id = movie_id
        self.page = page

        self.unrated_frame = tk.Toplevel(self.window)
        self.unrated_frame.geometry("300x200")
        self.unrated_frame.title("修改评分")

        self.txt = tk.StringVar()
        tk.Spinbox(self.unrated_frame, from_=1, to=5, textvariable=self.txt, width=5).place(x=85, y=80)
        tk.Button(self.unrated_frame, text="更新", command=self.rate).place(x=185, y=80)

    def rate(self):
        print("rate按钮被点击...")
        try:
            score = eval(self.txt.get())
            if isinstance(score, int) and 0 <= score <= 5:
                timestamp = int(time.time())

                con, cur = dbcon.mysqlcon.mysql_connect()
                if self.page == "edit":
                    sql = "update movrecsystem.ratings set userId={},movieId={},rating={},timestamp={} where userId={} and movieId={};".format(self.user_id, self.movie_id, score, timestamp, self.user_id, self.movie_id)
                else:
                    sql = "insert into movrecsystem.ratings values({},{},{},{});".format(self.user_id, self.movie_id, score, timestamp)
                cur.execute(sql)
                con.commit()
                dbcon.mysqlcon.mysql_close(con, cur)

                tk.messagebox.showinfo(title="更新成功", message="感谢您的评分！")
                self.unrated_frame.destroy()
            else:
                tk.messagebox.showwarning(title="更新失败", message="评分要为1-5的整数，请重新输入！")
        except:
            tk.messagebox.showwarning(title="更新失败", message="评分要为1-5的整数，请重新输入！")


class RatedFrame:
    def __init__(self, window, user_id, movie_id, rating, rated_time):
        self.window = window
        self.user_id = user_id
        self.movie_id = movie_id

        self.rated_frame = tk.Toplevel(self.window)
        self.rated_frame.geometry("300x200")
        self.rated_frame.title("我的评分")

        tk.Label(self.rated_frame, text="你的评分:{}\n评分时间:{}".format(rating, time.strftime("%Y-%m-%d %H:%M", time.localtime(rated_time)))).place(x=68, y=50)
        tk.Button(self.rated_frame, text="修改", command=self.modify).place(x=130, y=150)

    def modify(self):
        print("modify按钮被点击...")
        self.rated_frame.destroy()
        print("删除旧界面完成...")
        UnratedFrame(self.window, self.user_id, self.movie_id, "edit")
