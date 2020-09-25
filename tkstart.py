import os
import requests
import tkinter as tk
from tkactive import TkActive


class SpeechSynthesis():
    """
    该模块为语音合成的逻辑
    """
    def __init__(self):
        # 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
        # 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
        self.PER = 0
        # 语速，取值0-15，默认为5中语速
        self.SPD = 5
        # 音调，取值0-15，默认为5中语调
        self.PIT = 5
        # 音量，取值0-9，默认为5中音量
        self.VOL = 5
        # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
        self.AUE = 3

        FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
        self.FORMAT = FORMATS[self.AUE]

        self.CUID = "123456PYTHON"
        self.APIKEY = None
        self.SECRETKEY = None
        self.chats = None

    def getspeechsynthesis(self,filename=None,text=None,num=None,apikey=None,secretkey=None):

        """
        调用百度接口，合成语音
        param：{filename:生成的音频文件名称,text:所要转的字符文本,num:数字}
        return:None
        """
        TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
        params = {'grant_type': 'client_credentials',
                  'client_id': apikey,
                  'client_secret': secretkey
                  }
        result = requests.get(TOKEN_URL,params=params).json()
        access_token = result["access_token"]
        data = {'tok': access_token, 'tex': text, 'per': self.PER, 'spd': self.SPD, 'pit': self.PIT, 'vol': self.VOL, 'aue': self.AUE, 'cuid': self.CUID,
                  'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数
        headers = {"content-type":"application/json"}
        speech = requests.post('http://tsn.baidu.com/text2audio',headers=headers,data=data)
        with open(filename+str(num)+"."+self.FORMAT,"wb") as f:
            f.write(speech.content)

    def ergodic_file(self,ak=None,sk=None,filenames=None):
        for file_complete in filenames:
            file = file_complete.split("/")[-1]
            num = 0
            bool = file.endswith("txt")
            if bool or file.endswith("docx"):
                if bool:
                    file_prefix = file[:-4]
                else:
                    file_prefix = file[:-5]
                if bool:
                    f = open(file_complete, "r",encoding="utf-8")
                    while True:
                        text = f.read(2048)
                        if not text:
                            f.close()
                            break
                        else:
                            self.getspeechsynthesis(filename=file_prefix, text=text, num=num,apikey=ak,secretkey=sk)
                        num += 1
                else:
                    import docx
                    f = docx.Document(file_complete)
                    for paragraph in f.paragraphs:
                        self.getspeechsynthesis(filename=file_prefix, text=paragraph.text, num=num,apikey=ak,secretkey=sk)
                        num += 1

                copy_files = []
                for file_new in os.listdir("."):
                    if file_new.endswith("mp3") and file_new.startswith(file_prefix):
                        copy_files.append(file_new)
                parameter = "+".join(copy_files)
                status = os.system("copy /b {parameter} {file}.mp3".format(parameter=parameter,file=file_prefix))
                if not status:
                    for copy_file in copy_files:
                        os.unlink(copy_file)

class TkStart(TkActive):
    """
    开始合成页面
    """
    def __init__(self):
        super().__init__()
        self.cv = tk.Canvas(self.basic_frame, width=200, height=200, bg="#800080", border=0, highlightthickness=0)
        self.cv_ol = self.cv.create_oval(1, 1, 198, 198, fill="#EE82EE", outline="#EE82EE")

        self.label_cv_text = tk.StringVar(self)
        self.label_cv = tk.Label(self.cv, textvariable=self.label_cv_text, fg="black", bg="#EE82EE", font=("微软雅黑", 20))
        self.label_cv_text.set("合成中")
        #取消合成按钮
        self.synthesis_cancel = tk.Button(self.basic_frame,text="取消",fg="black", bg="red", font=("微软雅黑", 20),command=self.cancel)
        # 文字指针
        self.words_status = 0
        self.word_status_0_4 = True
        self.colors = ["Violet", "Magenta", "Fuchsia", "DarkMagenta", "Purple", "MediumOrchid", "DarkViolet",
                       "DarkOrchid",
                       "Indigo", "BlueViolet", "MediumPurple", "SlateBlue", "DarkSlateBlue", "Lavender", "GhostWhite",
                       "Blue", "MediumBlue", "MidnightBlue", "DarkBlue", "Navy", 'RoyalBlue', 'CornflowerBlue',
                       'LightSteelBlue',
                       'LightSlateGray', 'SlateGray', 'DodgerBlue', 'AliceBlue', 'SteelBlue', 'LightSkyBlue', 'SkyBlue',
                       'DeepSkyBlue',
                       'LightBlue', 'PowderBlue', 'CadetBlue', 'Azure', 'LightCyan', 'PaleTurquoise', 'Cyan', 'Aqua',
                       'DarkTurquoise',
                       'DarkSlateGray', 'DarkCyan', 'Teal', 'MediumTurquoise', 'LightSeaGreen', 'Turquoise',
                       'Aquamarine', 'MediumAquamarine',
                       'MediumSpringGreen', 'MintCream', 'SpringGreen', 'MediumSeaGreen', 'SeaGreen', 'Honeydew',
                       'LightGreen', 'PaleGreen',
                       'DarkSeaGreen', 'LimeGreen', 'Lime', 'ForestGreen', 'Green', 'DarkGreen', 'Chartreuse',
                       'LawnGreen', 'GreenYellow',
                       'DarkOliveGreen', 'YellowGreen', 'OliveDrab', 'Beige', 'LightGoldenrodYellow', 'Ivory',
                       'LightYellow', 'Yellow',
                       'Olive', 'DarkKhaki', 'LemonChiffon', 'PaleGoldenrod', 'Khaki', 'Gold', 'Cornsilk', 'Goldenrod',
                       'DarkGoldenrod',
                       'FloralWhite', 'OldLace', 'Wheat', 'Moccasin', 'Orange']
        # 颜色指针
        self.color_index = 0
        self.color_status_0_86 = True
        #停止状态指针
        self.run_status = True
        #over_button
        self.over_button = tk.Button(self.basic_frame,text="确定",fg="black", bg="green", font=("微软雅黑", 20),command=self.show_select_files)
        self.over_button_tips = tk.Label(self.basic_frame, text="完成!", fg="black", bg="#800080", font=("微软雅黑", 50))
    def noshow_select(self):
        super().noshow_key()
        self.run_button.place_forget()
        self.chats_listbox.place_forget()
        self.select_button.place_forget()
        self.delete_button.place_forget()
        self.chat_scrollbar_vertical.pack_forget()
        self.chat_scrollbar_horizontal.pack_forget()
        # 语音合成按钮
        self.start_button.place_forget()
        self.chats_listbox_tips.place_forget()

    def start(self):
        self.label_cv.place(relx=0.28, rely=0.35)
        self.cv.place(relx=0.3, rely=0.3)
        self.synthesis_cancel.place(relx=0.75,rely=0.45)
        #隐藏选择框
        self.noshow_select()
        #动态图
        self.displayColor()
        #调用合成api
        self.after(1000,self.synthesis)

    def synthesis(self):
        synthesis = SpeechSynthesis()
        synthesis.ergodic_file(ak=self.APIKEY, sk=self.SECRETKEY, filenames=self.chats)
        self.label_cv.place_forget()
        self.cv.place_forget()
        self.synthesis_cancel.place_forget()

        self.over_button.place(relx=0.45,rely=0.5)
        self.over_button_tips.place(relx=0.39,rely=0.3)

    def show_select_files(self):
        super().show_select_files()
        self.over_button_tips.place_forget()
        self.over_button.place_forget()
        self.chats.clear()
        self.chats_listbox.delete(0,tk.END)

    def cancel(self):
        self.run_status = False
        self.destroy()
        return TkVoice()

    def run(self):
        self.mainloop()

    def displayColor(self):
        if self.run_status == True:

            self.cv.itemconfigure(self.cv_ol, outline=self.colors[self.color_index], fill=self.colors[self.color_index])
            self.label_cv.configure(bg=self.colors[self.color_index])

            if self.words_status == 0:
                self.label_cv_text.set("合成中.")
            elif self.words_status == 1:
                self.label_cv_text.set("合成中..")
            elif self.words_status == 2:
                self.label_cv_text.set("合成中...")
            elif self.words_status == 3:
                self.label_cv_text.set("合成中....")
            else:
                self.label_cv_text.set("合成中.....")

            if self.word_status_0_4:
                self.words_status += 1
            else:
                self.words_status -= 1

            if self.words_status == 4:
                self.word_status_0_4 = False
            if self.words_status == 0:
                self.word_status_0_4 = True

            if self.color_status_0_86:
                self.color_index += 1
            else:
                self.color_index -= 1

            if self.color_index == 0:
                self.color_status_0_86 = True
            elif self.color_index == 86:
                self.color_status_0_86 = False

            self.after(30, self.displayColor)
if __name__ == '__main__':
    voice = TkStart()
    voice.run()