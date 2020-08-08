import tkinter as tk
import tkinter.messagebox
import dbcon.mysqlcon
import gui.home
import gui.user
import gui.search
import gui.movie


class LoginButton:
    def __init__(self, window, frame, bar, user_id, movie_id, page="H"):
        self.window = window
        self.frame = frame
        self.user_id = user_id
        self.movie_id = movie_id
        self.page = page
        txt1 = tk.StringVar()
        if self.user_id is None:
            txt1.set("登录")
        else:
            txt1.set("登出")
        self.button = tk.Button(bar, textvariable=txt1, command=self.respond)

    def respond(self):
        print("login按钮被点击...")
        if self.user_id is None:
            self.login()
        else:
            self.user_id = None
            self.update()

    def login(self):
        self.signup_frame = tk.Toplevel(self.window)
        self.signup_frame.geometry("350x250")
        self.signup_frame.title("登录")

        self.user = tk.StringVar()
        tk.Label(self.signup_frame, text="账号:").place(x=50, y=50)
        tk.Entry(self.signup_frame, textvariable=self.user).place(x=100, y=50)

        self.pwd = tk.StringVar()
        tk.Label(self.signup_frame, text="密码:").place(x=50, y=100)
        tk.Entry(self.signup_frame, textvariable=self.pwd, show='*').place(x=100, y=100)

        tk.Button(self.signup_frame, text="登录", command=self.confirm).place(x=250, y=150)

    def confirm(self):
        try:
            user = eval(self.user.get())
        except:
            tk.messagebox.showerror(message="账号必须是正整数!")
            return
        if isinstance(user, int) is False or user <= 0:
            tk.messagebox.showerror(message="账号必须是正整数!")
            return
        con, cur = dbcon.mysqlcon.mysql_connect()
        cur.execute("select pwd from movrecsystem.users where userId={}".format(user))
        result = cur.fetchall()
        if len(result) == 0:
            cur.execute("insert into movrecsystem.users values({},{})".format(user, self.pwd.get()))
            con.commit()
            tk.messagebox.showinfo(message="欢迎用户:{}!\n您是新用户!".format(user))
            self.signup_frame.destroy()
            self.user_id = user
            self.update()
        else:
            if result[0][0] == self.pwd.get():
                tk.messagebox.showinfo(message="欢迎用户:{}!\n您是老用户!".format(user))
                self.signup_frame.destroy()
                self.user_id = user
                self.update()
            else:
                tk.messagebox.showerror(message="密码错误!")

    def update(self):
        self.frame.destroy()
        print("删除旧界面完成...")
        new_frame = tk.Frame(self.window, width=800, height=650)
        new_frame.place(x=0, y=0, anchor='nw')
        if self.page == "H" or self.page == "U":
            gui.home.Home(self.window, new_frame, self.user_id, self.movie_id)
        elif self.page == "M":
            gui.movie.Movie(self.window, new_frame, self.user_id, self.movie_id)
        else:
            gui.search.Search(self.window, new_frame, self.user_id, self.movie_id)
        print("创建新home界面完成...")


class HomeButton:
    def __init__(self, window, frame, bar, user_id, movie_id):
        self.window = window
        self.frame = frame
        self.user_id = user_id
        self.movie_id = movie_id
        self.button = tk.Button(bar, text="主页", command=self.goto_home)

    def goto_home(self):
        print("home按钮被点击...")
        self.frame.destroy()
        print("删除旧界面完成...")
        new_frame = tk.Frame(self.window, width=800, height=650)
        new_frame.place(x=0, y=0, anchor='nw')
        gui.home.Home(self.window, new_frame, self.user_id, self.movie_id)
        print("创建新home界面完成...")


class UserButton:
    def __init__(self, window, frame, bar, user_id, movie_id):
        self.window = window
        self.frame = frame
        self.user_id = user_id
        self.movie_id = movie_id
        self.button = tk.Button(bar, text="我的", command=self.goto_user)

    def goto_user(self):
        print("user按钮被点击...")
        self.frame.destroy()
        print("删除旧界面完成...")
        new_frame = tk.Frame(self.window, width=800, height=650)
        new_frame.place(x=0, y=0, anchor='nw')
        gui.user.User(self.window, new_frame, self.user_id, self.movie_id)
        print("创建新user界面完成...")


class SearchButton:
    def __init__(self, window, frame, bar, user_id, movie_id):
        self.window = window
        self.frame = frame
        self.user_id = user_id
        self.movie_id = movie_id
        self.button = tk.Button(bar, text="搜索", command=self.goto_search)

    def goto_search(self):
        print("search按钮被点击...")
        self.frame.destroy()
        print("删除旧界面完成...")
        new_frame = tk.Frame(self.window, width=800, height=650)
        new_frame.place(x=0, y=0, anchor='nw')
        gui.search.Search(self.window, new_frame, self.user_id, self.movie_id)
        print("创建新search界面完成...")


# page值：H为home界面，U为user界面，S为search界面，M为movie界面
class NavBar:
    def __init__(self, window, frame, bar, user_id, movie_id, page):
        if user_id is not None:
            tk.Label(bar, text="当前用户:{}".format(user_id), font=("", 10)).pack(side='left')
            LoginButton(window, frame, bar, user_id, movie_id, page).button.pack(side="right")
            if page != "U":
                UserButton(window, frame, bar, user_id, movie_id).button.pack(side="right")
            if page != "H":
                HomeButton(window, frame, bar, user_id, movie_id).button.pack(side='right')
            if page != "S":
                SearchButton(window, frame, bar, user_id, movie_id).button.pack(side="right")
        else:
            LoginButton(window, frame, bar, user_id, movie_id, page).button.pack(side="right")
            if page == "M" or page == "S":
                HomeButton(window, frame, bar, user_id, movie_id).button.pack(side="right")
            if page != "S":
                SearchButton(window, frame, bar, user_id, movie_id).button.pack(side="right")
