
import time
from utils_xhr.threading import stop_thread
import re
import threading
import tkinter  # 使用Tkinter前需要先导入
import tkinter.messagebox
from queue import Queue
from tkinter import ttk
from annotate_xhr import threadingRun

from caculator_func import 计算2_近似配重计算器, 计算1_配重计算器, 等级品计算器_迭代计算, 等级品计算器_快速计算


class 重量计算器:
    # 组件创建
    def __init__(self, frame):
        scroll = tkinter.Scrollbar(frame)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.文本框计算结果 = tkinter.Text(frame, width=60, height=10, bg='white', yscrollcommand=scroll.set, wrap='none',
                                    font=('Arial', 14))
        scroll.config(command=self.文本框计算结果.yview)
        self.文本框计算结果.config(yscrollcommand=scroll.set)
        self.文本框计算结果.insert("insert",
                            "※使用说明\n1.精准配重:\n将列举所有单托净重1与单托净重2的配对方式,并且配对的纱线\n净重与设定的总净重要求完全相等\n2.近似配重:\n将列举所有单托净重1与单托净重2的配对方式,并且配对的纱线\n净重与设定的总净重要求近似且小于设定的总净重\n\n注意:请在下方输入具体公斤数(只允许是正整数,不可为小数)")
        self.文本框计算结果.pack(side='top')
        tkinter.Label(frame, text='总净重(kg)', font=('Arial', 14)).place(x=10, y=250)
        tkinter.Label(frame, text='单托净重1(kg)', font=('Arial', 14)).place(x=10, y=290)
        tkinter.Label(frame, text='单托净重2(kg)', font=('Arial', 14)).place(x=10, y=330)
        self.纱线总重 = tkinter.StringVar()
        self.纱线总重.set(30720)
        纱线总重_控件 = tkinter.Entry(frame, textvariable=self.纱线总重, font=('Arial', 14), width=13)
        纱线总重_控件.place(x=150, y=255)
        # 用户名
        self.整托净重1 = tkinter.StringVar()
        entry_usr_name = ttk.Combobox(frame, textvariable=self.整托净重1,width=10,font=('Arial', 14))
        entry_usr_name.place(x=150, y=335)
        entry_usr_name["value"] = (576,768,600,720)
        entry_usr_name.current(1)
        self.整托净重2 = tkinter.StringVar()
        entry_usr_pwd = ttk.Combobox(frame, textvariable=self.整托净重2, width=10, font=('Arial', 14))
        entry_usr_pwd.place(x=150, y=295)
        entry_usr_pwd["value"] = (576,768,600,720)
        entry_usr_pwd.current(0)
        # self.整托净重2.set(600)
        # entry_usr_pwd = tkinter.Entry(frame, textvariable=self.整托净重2, font=('Arial', 14), width=10)
        # entry_usr_pwd.place(x=150, y=295)
        btn_login = tkinter.Button(frame, text='精准配重', command=self.usr_login)
        btn_login.place(x=420, y=270)
        btn_sign_up = tkinter.Button(frame, text='近似配重', command=self.usr_sign_up)
        btn_sign_up.place(x=420, y=320)

    def usr_sign_up(self):
        a = self.整托净重1.get()
        b = self.整托净重2.get()
        c = self.纱线总重.get()
        self.文本框计算结果.delete(1.0, tkinter.END)
        # text.tag_config('tag', foreground='red')  # 设置tag即插入文字的大小,颜色等
        self.文本框计算结果.insert("insert", 计算2_近似配重计算器(a, b, c))

    # 第8步，定义用户登录功能
    def usr_login(self):
        # 这两行代码就是获取用户输入的usr_name和usr_pwd
        self.文本框计算结果.delete(1.0, tkinter.END)
        self.文本框计算结果.insert("insert", 计算1_配重计算器(self.整托净重1.get(), self.整托净重2.get(), self.纱线总重.get()))
class 等级品计算器:
    # 组件创建
    def __init__(self, frame):
        class Control:
            def __init__(self,frame):
                self.waitLabelValue = tkinter.StringVar()
                self.waitLabel = tkinter.Label(frame, textvariable=self.waitLabelValue, font=('Arial', 12), fg='red')
                self.waitLabel.place(x=250, y=250)
            @threadingRun(daemon=False)
            def show(self,text='',timeOut=-1):
                self.waitLabelValue.set(text)
                if timeOut!=-1:
                    time.sleep(timeOut)
                    self.waitLabelValue.set('')
        self.lock= threading.Condition()
        self.receiver_datas=None
        self.reC = re.compile(pattern=r'[^0-9^.]')
        self.正则表达式_匹配正小数或整数 = re.compile(pattern=r'^(\d+)(\.\d+)?$')
        self.正则表达式_匹配整数 = re.compile(pattern=r'^(-?)(\d+)?$')
        self.excuteThread=None
        self.control=Control(frame)
        self.receiver=Queue()
        t1=threading.Thread(target=self.receive)
        t1.setDaemon(True)
        t1.start()
        self.dataFrame = None
        self.dataRemoveFrame = None
        self.frame = frame
        scroll = tkinter.Scrollbar(frame)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scrollX = tkinter.Scrollbar(frame)
        scrollX.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.文本框计算结果 = tkinter.Text(frame, width=60, height=10, bg='white',xscrollcommand=scrollX.set, yscrollcommand=scroll.set, wrap='none',
                                    font=('Arial', 14))
        self.文本框计算结果.tag_config('tag_gray',foreground = '#696969')
        self.文本框计算结果.tag_config('tag_red_font',foreground = 'red')
        self.文本框计算结果.config(wrap=tkinter.WORD)
        scroll.config(command=self.文本框计算结果.yview)
        self.文本框计算结果.config(yscrollcommand=scroll.set,xscrollcommand=scrollX.set)
        self.文本框计算结果.insert("insert",
                            "※使用说明\n此软件用于配重等级品\n"
                            "【添加数据】用于添加需要计算的数据组(一行代表一个数据)\n"
                            "【添加排除数据】用于添加不需要纳入计算的数据组(一行代表一个数据)\n"
                            "【托数】用于限定托数当托数为-1的时候，会计算所有情况\n"
                            "【快速计算】用于计算：速度较快，数据量大的时候推荐使用\n"
                            "【迭代计算】用于计算：准确性较高，数据量小的时候推荐使用，数据量大的时候不推荐\n"
                            "\n注意:推荐使用【快速计算】"
                            )
        self.文本框计算结果.pack(side='top')
        self.文本框计算结果['state'] = tkinter.DISABLED
        tkinter.Label(frame, text='重量不超过(kg)', font=('Arial', 14)).place(x=5, y=250)
        tkinter.Label(frame, text='托数(个)', font=('Arial', 14)).place(x=5, y=290)
        self.btn_simple = tkinter.Button(frame, text='快速计算', command=self.cauculate_quick)
        self.btn_simple.place(x=70, y=330)
        self.btn_flex = tkinter.Button(frame, text='迭代计算', command=self.cauculate_flex)
        self.btn_flex.place(x=150, y=330)
        self.btn_stop = tkinter.Button(frame, text='停止运算', command=self.cauculate_stop)
        self.btn_stop['state'] = tkinter.DISABLED
        self.btn_stop.place(x=230, y=330)
        self.btn_datas = tkinter.Button(frame, text='添加数据', command=self.bombFrame)
        self.btn_datas.place(x=400, y=250)
        self.btn_remove_datas = tkinter.Button(frame, text='添加排除数据', command=self.bombFrameRemove)
        self.btn_remove_datas.place(x=400, y=300)
        # 用户名
        self.重量不超过 = tkinter.StringVar()
        self.重量不超过.set(3333)
        self.entry_usr_name = tkinter.Entry(frame, textvariable=self.重量不超过, font=('Arial', 14), width=9)
        self.entry_usr_name.place(x=150, y=250)
        # 用户密码
        self.托数 = tkinter.StringVar()
        self.托数.set(-1)
        self.entry_usr_pwd = tkinter.Entry(frame, textvariable=self.托数, font=('Arial', 14), width=5)
        self.entry_usr_pwd.place(x=150, y=290)

        # 弹窗
        self.dataFrame = tkinter.Toplevel(self.frame)
        self.dataFrame.resizable(width=False,height=False)
        self.dataFrame.geometry('%dx%d+%d+%d' % (120, 400, 600, 0))
        self.dataFrame.attributes("-toolwindow", 2)  # 去掉窗口最大化最小化按钮，只保留关闭
        self.dataFrame.title('以下是计算数据')
        self.dataFrame.protocol("WM_DELETE_WINDOW", lambda: self.closeBombFrame(self.dataFrame))
        scroll = tkinter.Scrollbar(self.dataFrame)
        self.弹框数据文本框组件_源数据 = tkinter.Text(self.dataFrame, width=9, height=200, bg='white',
                                          yscrollcommand=scroll.set, wrap='none',
                                          font=('Arial', 14))
        self.弹框数据文本框组件_源数据.insert('insert','净重\n660.00\n658.50\n658.50\n658.50\n658.50\n658.50\n658.50\n658.50\n658.50\n657.50\n657.50\n657.50\n657.50\n657.50\n656.50\n655.50\n655.50\n655.50\n655.50\n655.50\n653.50\n652.50\n652.50\n650.50\n649.50\n630.50\n619.50\n610.50\n608.50\n607.50\n604.50\n597.50\n590.50\n586.50\n585.50\n584.50\n577.50\n567.50\n565.50\n558.50\n553.50\n548.50\n546.50\n545.50\n541.50\n539.50\n534.50\n525.50\n516.50\n510.50\n506.50\n499.50\n486.50\n479.50\n474.50\n470.50\n363.00\n336.50\n331.50\n')
        tkinter.Button(self.dataFrame, text='clear', bg='#f7acbc', width=7,
                            command=lambda: self.clear(self.弹框数据文本框组件_源数据)).place(x=0, y=0)  # , command=self.usr_login
        tkinter.Button(self.dataFrame, text='↓↓↓', width=7,command=lambda:self.runButton(self.弹框数据文本框组件_源数据)).pack(side='top', anchor='e')
        scroll.config(command=self.弹框数据文本框组件_源数据.yview)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.弹框数据文本框组件_源数据.pack(side='top')
        # .place(x=0, y=30)
        self.dataFrame.withdraw()
        self.dataRemoveFrame = tkinter.Toplevel(self.frame)
        self.dataRemoveFrame.resizable(width=False, height=False)
        self.dataRemoveFrame.geometry('%dx%d+%d+%d' % (120, 400, 720, 0))
        self.dataRemoveFrame.attributes("-toolwindow", 2)  # 去掉窗口最大化最小化按钮，只保留关闭
        self.dataRemoveFrame.title('以下是将被排除的数据')
        self.dataRemoveFrame.protocol("WM_DELETE_WINDOW", lambda: self.closeBombFrame(self.dataRemoveFrame))
        scrollR = tkinter.Scrollbar(self.dataRemoveFrame)
        self.弹框数据文本框_剔除数据 = tkinter.Text(self.dataRemoveFrame, width=9, height=100, bg='white',
                                         yscrollcommand=scrollR.set, wrap='none', fg='red',
                                         font=('Arial', 14))
        tkinter.Button(self.dataRemoveFrame, text='clear', bg='#f7acbc', width=7,
                       command=lambda: self.clear(self.弹框数据文本框_剔除数据)).place(x=0,y=0)  # , command=self.usr_login
        tkinter.Button(self.dataRemoveFrame, text='↓↓↓', width=7,
                       command=lambda: self.runButton(self.弹框数据文本框_剔除数据)).pack(side='top', anchor='e')

        scrollR.config(command=self.弹框数据文本框_剔除数据.yview)
        scrollR.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        # self.弹框数据文本框_剔除数据.configure(bg='red' )

        self.弹框数据文本框_剔除数据.pack(side='top')
        self.dataRemoveFrame.withdraw()
    def runButton(self,text):
        text.see(tkinter.END)
    def clear(self,text):
        text.delete(1.0, tkinter.END)
    def receive(self):
        self.receiver_datas={'showArr':[]}
        reWeight=re.compile(pattern=r'重量差为:(.*?);')
        self.receiver_datas.setdefault('state',0)#0未执行。1正在执行
        self.receiver_datas.setdefault('showNumArr',None)#0未执行。1正在执行
        def insertText(showArr):
            self.文本框计算结果['state'] = tkinter.NORMAL
            if len(showArr) in self.receiver_datas.get('showNumArr') or self.receiver_datas['state']==0:
                self.文本框计算结果.delete(1.0, tkinter.END)
                for i in range(len(showArr)):
                    if i%2==1:
                        if showArr[i][0] == 0:
                            begin = showArr[i][1][1].find('重量差为:0.0')
                            self.文本框计算结果.insert('end', showArr[i][1][1][0:begin] , 'tag_gray')
                            self.文本框计算结果.insert('end', showArr[i][1][1][begin:begin + 8]  , 'tag_red_font')
                            self.文本框计算结果.insert('end', showArr[i][1][1][begin + 8:len(showArr[i][1][1])] + '\n' , 'tag_gray')
                        else:
                            self.文本框计算结果.insert('end', showArr[i][1][1]+'\n' , 'tag_gray')
                    else:
                        if showArr[i][0] == 0:
                            begin = showArr[i][1][1].find('重量差为:0.0')
                            self.文本框计算结果.insert('end', showArr[i][1][1][0:begin])
                            self.文本框计算结果.insert('end', showArr[i][1][1][begin:begin + 8], 'tag_red_font')
                            self.文本框计算结果.insert('end', showArr[i][1][1][begin + 8:len(showArr[i][1][1])] + '\n')
                        else:
                            self.文本框计算结果.insert('end', showArr[i][1][1]+'\n')


            self.文本框计算结果['state'] = tkinter.DISABLED
        def connect(line):
            if line[0]=='start':
                self.receiver_datas['showNumArr'] = [1, 3, 4, 7, 11, 18, 29, 47,76,100]
                self.receiver_datas['state']=1
                return None
            if line[0] == 'end':
                self.receiver_datas['state'] = 0
                insertText(self.receiver_datas['showArr'])
                self.receiver_datas['showArr']=[]
                return None
            return line
        i=0
        while True:
            line=self.receiver.get()
            line=connect(line)
            # print(line)
            if line:
                newLine = (float(re.findall(reWeight, line[1])[0]), line)
                if len(self.receiver_datas['showArr'])<=100:
                    self.receiver_datas['showArr'].append(newLine)
                    self.receiver_datas['showArr']=sorted(self.receiver_datas['showArr'],key=lambda x:x[0])
                else:
                    if self.receiver_datas['showArr'][-1][0]>newLine[0]:
                        self.receiver_datas['showArr'].append(newLine)
                        self.receiver_datas['showArr'] = sorted(self.receiver_datas['showArr'], key=lambda x: x[0])[0:100]
                insertText(self.receiver_datas['showArr'])
    def closeBombFrame(self, frame):
        frame.withdraw()
    @threadingRun(daemon=False)
    def bombWiait(self,text):
        self.control.show(text='计算中....')
        if self.excuteThread!=None:
            if self.excuteThread.is_alive():
                self.excuteThread.join()
        self.control.show(text='计算完成!')
        if self.receiver_datas.get('state')==0:
            # print(self.receiver_datas.get('state'))
            if self.文本框计算结果.get("1.0","end").strip()=="":
                self.文本框计算结果['state'] = tkinter.NORMAL
                self.文本框计算结果.delete(1.0, tkinter.END)
                self.文本框计算结果.insert('insert','没有计算结果~建议更换组合计算(*^▽^*)')
                self.文本框计算结果['state'] = tkinter.DISABLED

        self._revocerComponentUse()

    def bombFrameRemove(self):
        self.dataRemoveFrame.update()
        self.dataRemoveFrame.deiconify()

    def bombFrame(self):
        self.dataFrame.update()
        self.dataFrame.deiconify()

    def _getDatas(self):
        def getDatas(datasStr, reC=''):
            datas = datasStr.strip().split('\n')
            arr = map(lambda x: re.sub(pattern=reC, string=x, repl=''), datas)
            arr = filter(lambda x: x != '', arr)
            return list(map(lambda x: float(x), arr))
        datas = []
        remove_datas = []
        if self.弹框数据文本框组件_源数据:
            datasStr = self.弹框数据文本框组件_源数据.get("0.0", "end")
            datas = getDatas(datasStr, self.reC)
        if self.弹框数据文本框_剔除数据:
            datasRemoveStr = self.弹框数据文本框_剔除数据.get("0.0", "end")
            remove_datas = getDatas(datasRemoveStr, self.reC)
        return (datas, remove_datas)

    @threadingRun(daemon=False)
    def cauculate_flex(self):
        # 等级品计算器_迭代计算

        self._banComponentUse()
        data_tup = self._getDatas()
        # 等级品计算器_快速计算()
        # 开启转圈
        if self._checkInput(data_tup, self.重量不超过.get(), self.托数.get()):
            t = threading.Thread(target=等级品计算器_迭代计算,
                                 kwargs={'src_datas': data_tup[0], 'remove_datas': data_tup[1],
                                         'limitWeight': float(self.重量不超过.get()), 'num': int(self.托数.get()),
                                         'receiver': self.receiver})
            t.setDaemon(True)
            self.excuteThread = t
            t.start()
            self.btn_stop['state'] = tkinter.NORMAL
            self.bombWiait('计算中...')
        else:
            self.control.show('数据输入有误!')
            # self.receiver.put((0,'数据输入有误！'))
            self._revocerComponentUse()
    # @threadingRun
    def cauculate_stop(self):
        if self.excuteThread!=None:
            if self.excuteThread.is_alive():
                stop_thread(self.excuteThread)
            while self.receiver.qsize()!=0:
                self.receiver.get(timeout=0.1)
            self.receiver.put(('end',))
            self._revocerComponentUse()
            self.control.show('已中止计算!')
    def _banComponentUse(self):
        self.文本框计算结果['state'] = tkinter.NORMAL
        self.文本框计算结果.delete(1.0, tkinter.END)
        self.文本框计算结果['state'] = tkinter.DISABLED
        # self.文本框计算结果.insert()


        self.entry_usr_name['state']=tkinter.DISABLED
        self.entry_usr_pwd['state']=tkinter.DISABLED
        self.btn_simple['state']=tkinter.DISABLED
        self.btn_flex ['state']=tkinter.DISABLED
        # btn_stop = tkin
        self.btn_datas['state']=tkinter.DISABLED
        self.btn_remove_datas['state']=tkinter.DISABLED
        # self.文本框计算结果['state']=tkinter.DISABLED
    def _revocerComponentUse(self):
        self.entry_usr_name['state'] = tkinter.NORMAL
        self.entry_usr_pwd['state'] = tkinter.NORMAL
        self.文本框计算结果['state'] = tkinter.NORMAL
        self.btn_simple['state'] = tkinter.NORMAL
        self.btn_flex['state'] = tkinter.NORMAL
        self.btn_stop['state'] = tkinter.DISABLED
        self.btn_datas['state'] = tkinter.NORMAL
        self.btn_remove_datas['state'] = tkinter.NORMAL
        # self.btn_datas
    def _checkInput(self,a,b,c):
        # b=re.match(self.reC,b)
        if re.fullmatch(self.正则表达式_匹配正小数或整数,b)==None:
            return False
        if re.fullmatch(self.正则表达式_匹配整数,c)==None:
            return False
        return True
    @threadingRun(daemon=False)
    def cauculate_quick(self):
        self._banComponentUse()
        data_tup = self._getDatas()
        # 等级品计算器_快速计算()
        if self._checkInput(data_tup,self.重量不超过.get(),self.托数.get()):
            t = threading.Thread(target=等级品计算器_快速计算,
                                 kwargs={'src_datas': data_tup[0], 'remove_datas': data_tup[1],
                                         'limitWeight': float(self.重量不超过.get()), 'num': int(self.托数.get()),'receiver':self.receiver})
            t.setDaemon(True)
            self.excuteThread=t
            t.start()
            self.btn_stop['state'] = tkinter.NORMAL
            self.bombWiait('计算中...')
        else:
            self.control.show('数据输入有误!')
            self._revocerComponentUse()
class 选项卡:
    def __init__(self, frame, tabName=['1', '2', '3']):
        tab = ttk.Notebook(frame)
        self.frames = []
        for i in range(len(tabName)):
            frame1 = tkinter.Frame(tab)
            tab.add(frame1, text=tabName[i])
            self.frames.append(frame1)
        # frame2 = tkinter.Frame(tab, bg="yellow")
        # tab2 = tab.add(frame2, text="2")
        # frame3 = tkinter.Frame(tab, bg="blue")
        # tab3 = tab.add(frame3, text="3")
        tab.pack(expand=True, fill=tkinter.BOTH)
        tab.select(self.frames[0])
class 信息:
    def __init__(self, frame):
        tkinter.Label(frame, text='软件网址:https://github.com/jhfwb/calculator_BILLION', font=('Arial', 14)).place(x=10, y=10)
        tkinter.Label(frame, text='bug反馈邮箱:527077832@qq.com', font=('Arial', 14)).place(x=10, y=50)
        tkinter.Label(frame, text='时间:', font=('Arial', 14)).place(x=10, y=90)
        # https: // github.com / jhfwb / calculator_BILLION

if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('纱线配重计算器_1.0.0.0')
    # 第3步，设定窗口的大小(长 * 宽)
    window.geometry('550x400+20+20')  # 这里的乘是小x
    a = 选项卡(window, tabName=['重量计算器', '等级品配重','信息'])
    重量计算器(a.frames[0])
    等级品计算器(a.frames[1])
    信息(a.frames[2])
    # for frame in a.frames:
    #     重量计算器(frame)
    window.mainloop()
# 第10步，主窗口循环显示
