import tkinter as tk
import gui.home

window = tk.Tk()
window.geometry("800x650")
window.title("Movie Recommendation System -by wdy")
frame = tk.Frame(window, width=800, height=650)
frame.place(x=0, y=0, anchor="nw")
gui.home.Home(window, frame, None, None)
window.mainloop()
