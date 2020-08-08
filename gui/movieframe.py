import tkinter as tk
import time
import gui.movie
import gui.method


# page值：N为None没有指定界面，U为user界面，M为movie界面
class MovieFrame:
    def __init__(self, window, frame, movie_frame, user_id, movie_id, page="N", **kw):
        self.window = window
        self.frame = frame
        self.user_id = user_id
        self.movie_id = movie_id

        url = gui.method.get_url(self.movie_id)
        img_url, title, date, genres = gui.method.get_src(url, self.movie_id)
        self.info_frame = tk.Frame(movie_frame, width=90, height=120)

        if page == "U":
            tk.Label(self.info_frame, text="评分:{}".format(kw['rating']), font=('', 10)).pack()
            tk.Label(self.info_frame, text="时间:{}".format(time.strftime('%Y-%m-%d', time.localtime(kw['time']))), font=('', 10)).pack()

        if page == "M":
            tk.Label(self.info_frame, text="相似度:{:.2f}".format(kw['simDegree']), font=('', 9)).pack()

        self.photo_image = gui.method.get_image(img_url)
        self.button = tk.Button(self.info_frame, image=self.photo_image, width=65, height=95, bg="white", command=self.goto_movie)
        self.button.pack()

        tk.Label(self.info_frame, text="{}".format(title), width=20, height=1, font=('', 10)).pack()
        tk.Label(self.info_frame, text="{}".format(date), width=20, height=1, font=('', 10)).pack()

    def goto_movie(self):
        print("movie按钮被点击...")
        self.frame.destroy()
        print("删除旧界面完成...")
        new_frame = tk.Frame(self.window, width=800, height=640)
        new_frame.place(x=0, y=0, anchor="nw")
        gui.movie.Movie(self.window, new_frame, self.user_id, self.movie_id)
        print("创建新movie界面完成...")
