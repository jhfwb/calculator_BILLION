from tkinter import *
import tkinter
import webbrowser
root = Tk()
root.title("Jason niu工作室")
theLabel=tkinter.Label(root,text="进入GUI世界，请开始你的表演！\n(点击下边链接即可访问我们官方网站)")
theLabel.pack()
text = Text(root,width=33,height=5)
text.pack()
text.insert(INSERT,"欢迎访问Jason niu工作室官方网站")
text.tag_add("link","1.4","1.15")
text.tag_config("link",foreground="blue",underline=True)
def show_arrow_cursor(event):
    text.config(cursor="arrow")
def show_xterm_cursor(event):
    text.config(cursor="xterm")
def click(event):
    webbrowser.open("http://jason-niu.com")
text.tag_bind("link","",show_arrow_cursor)
text.tag_bind("link","",show_xterm_cursor)
text.tag_bind("link","",click)
root.mainloop()
