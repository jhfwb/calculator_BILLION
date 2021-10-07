import threading
import tkinter
import tkinter.ttk
class MyProgressbar:
    def __init__(self,frame,width=50,x=0,y=0):
        self.x=x
        self.y=y
        self.__showFlag=True
        self.frame=frame
        self.width=width
        self.progressbarOne = tkinter.ttk.Progressbar(frame, length=width, mode='indeterminate',
                                                      orient=tkinter.HORIZONTAL)
        self.progressbarOne['maximum'] = width
        self.progressbarOne['value'] = 0
        self.progressbarOne.start(10)
        t = threading.Thread(target=self.waitClose)
        t.setDaemon(True)
        t.start()
    def waitClose(self):
        while self.__showFlag:
            if self.__showFlag==False:
                self.progressbarOne.destroy()
    def show(self):
        self.progressbarOne.place(x=self.x,y=self.y)
    def hide(self):
        self.progressbarOne.place_forget()
if __name__ == '__main__':

    root = tkinter.Tk()
    root.geometry('150x120')
    p=MyProgressbar(root)
    button = tkinter.Button(root, text='Running', command=lambda :MyProgressbar.show(p))
    button2 = tkinter.Button(root, text='stop', command=lambda :MyProgressbar.hide(p))
    button.pack(pady=5)
    button2.pack(pady=5)
    root.mainloop()