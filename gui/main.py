import tkinter as tk
import gui.home
# import gui.user
# import gui.search
# import gui.movie

# 测试home.py页面
window = tk.Tk()
window.geometry("800x650")
window.title("Movie Recommendation System -by wdy")
frame = tk.Frame(window, width=800, height=650)
frame.place(x=0, y=0, anchor="nw")
gui.home.Home(window, frame, None, None)
window.mainloop()

# 测试user.py页面
'''window = tk.Tk()
window.geometry("800x650")
window.title("Movie Recommendation System -proudly produced by wdy")
frame = tk.Frame(window, width=800, height=650)
frame.place(x=0, y=0, anchor="nw")
gui.user.User(window, frame, 1, 1)
window.mainloop()'''

# 测试search.py页面
'''window = tk.Tk()
window.geometry("800x650")
window.title("Movie Recommendation System -proudly produced by wdy")
frame = tk.Frame(window, width=800, height=650)
frame.place(x=0, y=0, anchor="nw")
gui.search.Search(window, frame, 1, None)
window.mainloop()'''

# 测试movie.py页面
'''window = tk.Tk()
window.geometry("800x650")
window.title("Movie Recommendation System -proudly produced by wdy")
frame = tk.Frame(window, width=800, height=650)
frame.place(x=0, y=0, anchor="nw")
gui.movie.Movie(window, frame, 1, 2)
window.mainloop()'''
