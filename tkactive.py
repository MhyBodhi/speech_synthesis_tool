import tkinter as tk
from tkinter import filedialog
from tkbasic import TkBasic

class TkActive(TkBasic):
    """
    选择语音合成文件模块
    """
    def __init__(self):
        super().__init__()
        self.chats = set()
        # 选择合成列表
        self.chats_listbox = tk.Listbox(self.basic_frame, height=24, width=30, selectmode=tk.EXTENDED)
        #提示
        self.chats_listbox_tips = tk.Label(self.basic_frame,text="选择语音合成文件列表",bg="#800080",fg="black",font=("微软雅黑",10,"bold"))
        #开始语音合成
        self.start_button = tk.Button(
            self.basic_frame, text="start", bg="green",
            fg="black", command=self.start,state="disable",
            font=("微软雅黑", 15))
        #选择元素索引
        self.chats_indexs = None
        #文件选择按钮
        self.select_button = tk.Button(
            self.basic_frame, text="选择\n原文件", bg="green",
            fg="black", command=self.select_files,
            font=("微软雅黑", 10))
        #删除按钮
        self.delete_button = tk.Button(
            self.basic_frame, text="删除", bg="green",
            fg="black", command=self.delete_files,
            font=("微软雅黑", 10))
        self.delete_button.configure(state="disable")
        # 滚动条
        self.chat_scrollbar_vertical = tk.Scrollbar(self.chats_listbox, orient="vertical", command=self.chats_listbox.yview)
        self.chat_scrollbar_horizontal = tk.Scrollbar(self.chats_listbox, orient="horizontal", command=self.chats_listbox.xview)
        self.chats_listbox.config(yscrollcommand=self.chat_scrollbar_vertical.set)
        self.chats_listbox.config(xscrollcommand=self.chat_scrollbar_horizontal.set)

        # 绑定事件
        self.chats_listbox.bind("<1>", self.listenChats)
        self.chats_listbox.bind("<3>", self.listenChats)
        self.chats_listbox.bind("<Control-a>", self.listenChats)
        # self.chats_listbox.bind("<Shift-Button-1>", self.listenChats)

    def show_select_files(self):
        super().noshow_key()
        self.run_button.place_forget()
        self.chats_listbox.place(x=100, y=30,relwidth=0.5, relheight=0.8)
        self.select_button.place(relx=0.1, rely=0.3, relwidth=0.1, relheight=0.15)
        self.delete_button.place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.1)
        self.chat_scrollbar_vertical.pack(side="right", fill="y")
        self.chat_scrollbar_horizontal.pack(side="bottom", fill="x")
        #语音合成按钮
        self.start_button.place(relx=0.7, rely=0.35, relwidth=0.13, relheight=0.1)
        self.chats_listbox_tips.place(x=100, y=5)

    def select_files(self):
        filenames = filedialog.askopenfilenames()
        for file in filenames:
            self.chats.add(file)
        self.chats_listbox.delete(0,tk.END)
        for file in self.chats:
            self.chats_listbox.insert(0,file)
        if self.chats:
            self.start_button.configure(state="active")

    def delete_files(self):
        for index in self.chats_indexs:
            self.chats.discard(self.chats_listbox.get(index))
        # 更新监控列表
        self.chats_listbox.delete(0, tk.END)
        for chat in self.chats:
            self.chats_listbox.insert(0, chat)
        if self.chats:
            self.start_button.configure(state="active")
        else:
            self.start_button.configure(state="disable")

    def listenChats(self,event):
        self.chats_indexs = self.chats_listbox.curselection()
        if self.chats_indexs:
            self.delete_button.configure(state="active")
        else:
            self.delete_button.configure(state="disable")

    def start(self):
        raise Exception

if __name__ == '__main__':
    start = TkActive()
    start.mainloop()