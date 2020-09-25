import os
import sqlite3
import time
import tkinter as tk
import requests

class TkBasic(tk.Tk):
    """
    GUI 基本模块:百度key验证、数据库交互
    """
    def __init__(self):
        super().__init__()
        self.basic_frame = tk.Frame(self, bg="#800080")
        self.basic_frame.place(relx=0,rely=0,relheight=1,relwidth=1)
        self.title("语音小工具")
        #开始语音合成入口
        self.start_text = tk.StringVar(self)
        self.start_text.set("开始")
        #api_key提示文本
        self.api_key_tips = tk.StringVar(self)
        self.api_key_tips.set("请输入百度api_key")
        #secret_key提示文本
        self.secret_key_tips = tk.StringVar(self)
        self.secret_key_tips.set("请输入百度secret_key")
        x = self.winfo_screenmmwidth()
        y = self.winfo_screenheight()
        self.geometry("500x500+%d+%d" % (x, y / 2 * 0.5))
        self.resizable(0, 0)
        self.run_button = tk.Button(
                self.basic_frame,textvariable=self.start_text, bg="green",
                fg="black",command=self.show_start_button,
                font=("微软雅黑", 20))
        self.run_button.place(relx=0.35,rely=0.5,relheight=0.1,relwidth=0.3)
        #api_key输入框
        self.api_key = tk.Entry(self.basic_frame, textvariable=self.api_key_tips)
        self.api_key.place_forget()
        #secret_key输入框
        self.secret_key = tk.Entry(self.basic_frame, textvariable=self.secret_key_tips)
        self.secret_key.place_forget()
        #提示
        self.label_showapi = tk.Label(self.basic_frame, text="百度AK:", bg="blue",font=("微软雅黑",12,"bold"))
        self.label_showsecret = tk.Label(self.basic_frame, text="百度SK:", bg="blue",font=("微软雅黑",12,"bold"))
        #验证按钮
        self.verify_button = tk.Button(
            self.basic_frame, text="验证", bg="green",
            fg="black", command=self.get_access_token,
            font=("微软雅黑", 10))
        #提示验证信息
        self.verify_info_text = tk.StringVar(self)
        self.verify_info = tk.Label(self.basic_frame,textvariable=self.verify_info_text,bg="blue",font=("微软雅黑",10,"bold"))
        self.start_info = tk.Label(self.basic_frame,text="网络连接失败,请检查网络是否正常...",bg="blue",fg="red",font=("微软雅黑",15,"bold"))

        self.APIKEY = None
        self.SECRETKEY = None
        # 创建表语句
        self.sql_create = """CREATE TABLE key
                               (api_key           TEXT    NOT NULL,
                                secret_key        TEXT    NOT NULL);"""
        #插入语句
        self.sql_insert = "insert into key values(?,?)"
        # 更新语句
        self.sql_update = "update key set api_key=%s,secret_key=%s" % (self.APIKEY, self.SECRETKEY)
        # 查询语句
        self.sql_select = "select api_key,secret_key from key"
        # 删除语句
        self.sql_delete = "delete from key"

    def show_start_button(self):
        if self.run_button["text"] == "开始":
            if os.path.exists("save_database.db"):
                keys = self.runQuery(self.sql_select,namedb="save_database.db",receive=True)
                if keys:
                    self.APIKEY = keys[0][0]
                    self.SECRETKEY = keys[0][1]
                    status = os.system("ping www.baidu.com -n 3 > test.txt")
                    if not status:
                        access_token = self.access_token()
                        if access_token:
                            self.show_select_files()
                        else:
                            self.runQuery(self.sql_delete,namedb="save_database.db")
                            self.show_key()
                    else:
                        self.start_info.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.8)
                else:
                    self.show_key()
            else:
                self.runQuery(self.sql_create,namedb="save_database.db")
                self.show_key()
        else:
            self.noshow_key()

    def show_key(self):

        self.start_text.set("取消")
        self.run_button.configure(fg="red")
        # api_key
        self.api_key.place(relx=0.2, rely=0.2, relheight=0.05, relwidth=0.3)
        self.secret_key.place(relx=0.2, rely=0.3, relheight=0.05, relwidth=0.3)

        self.label_showapi.place(relx=0.05, rely=0.2)
        self.label_showsecret.place(relx=0.05, rely=0.3)
        #验证
        self.verify_button.place(relx=0.6,rely=0.23,relwidth=0.1,relheight=0.1)

    def noshow_key(self):
        self.start_text.set("开始")
        self.run_button.configure(fg="black")
        # api_key
        self.api_key.place_forget()
        self.secret_key.place_forget()

        self.label_showapi.place_forget()
        self.label_showsecret.place_forget()
        # 验证
        self.verify_button.place_forget()
        self.verify_info.place_forget()
        #start_info
        self.start_info.place_forget()

    def get_access_token(self):
        self.APIKEY = self.api_key.get()
        self.SECRETKEY = self.secret_key.get()
        status = os.system("ping www.baidu.com -n 3 > test.txt")
        if not status:
            access_token = self.access_token()
            if access_token:
                self.verify_info.place(relx=0.7,rely=0.23)
                self.verify_info_text.set("验证成功...\n开始进入合成界面")
                self.verify_info.configure(fg="blacK")
                self.runQuery(self.sql_insert,data=(self.APIKEY,self.SECRETKEY),namedb="save_database.db")
                self.after(1000)
                self.show_select_files()
            else:
                self.verify_info.place(relx=0.7, rely=0.23)
                self.verify_info_text.set("验证失败...\n请确认密钥是否正确")
                self.verify_info.configure(fg="red")
        else:
            self.verify_info.place(relx=0.7, rely=0.23)
            self.verify_info_text.set("网络异常...")
            self.verify_info.configure(fg="red")
            tk.after(2000)
            self.noshow_key()

    def access_token(self):
        TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
        params = {'grant_type': 'client_credentials',
                  'client_id': self.APIKEY,
                  'client_secret': self.SECRETKEY
                  }
        result = requests.get(TOKEN_URL, params=params).json()
        try:
            access_token = result["access_token"]
            return access_token
        except:
            return False

    def show_select_files(self):
        raise Exception

    def runQuery(self,sql, data=None, receive=False, namedb=None):
        conn = sqlite3.connect(namedb)
        cursor = conn.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        if receive:
            return cursor.fetchall()
        else:
            conn.commit()
        conn.close()

if __name__ == '__main__':
    tk = TkBasic()
    tk.mainloop()