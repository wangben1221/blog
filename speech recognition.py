# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_baidu_gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from aip import AipSpeech
import uuid
import pyaudio
import wave
import time


from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
# 获取本机MAC
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])  # 以“：”为间隔。'98:fa:9b:22:38:72'
class Ui_MainWindow():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(80, 60, 321, 251))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 340, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 340, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_2.clicked.connect(MainWindow.close)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)###连接信号与槽函数
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "开始识别"))
        self.pushButton_2.setText(_translate("MainWindow", "结束"))






    # 读取音频文件
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:  # 读模式打开
            return fp.read()  # 读取

    # 本地语音识别
    def aip_get_asrresult(self,client, afile, afmt):
        # 识别结果已经被SDK由JSON字符串转为dict
        result = client.asr(self.get_file_content(afile), afmt, 16000, {"cuid": CUID, "dev_pid": DEV_PID, })
        # print(result)
        if result["err_msg"] == "success.":
            print(result["result"])
            return result["result"]
        else:
            print(result["err_msg"])
            return ""

    # 用Pyaudio库录制音频
    def audio_record(self,out_file, rec_time):  # out_file是保存地址
        CHUNK = 1024#缓存，能存多少个采样点
        FORMAT = pyaudio.paInt16#format=paInt16采样深度是两个字节
        CHANNELS = 1#声道
        RATE = 16000#采样率
        # RECORD_SECONDS = 5
        # WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()
        # 声卡打开读文件
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("Start Recording...")
        self.printf("Start Recording...")

        frames = []
        # 录制音频数据
        for i in range(0, int(RATE / CHUNK * rec_time)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Recording Done...")
        self.printf("Recording Done...")
        # 保存音频文件
        wf = wave.open('audio_output.wav', 'wb')  # out_file是保存地址
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


    def printf(self, mypstr):
        # ###
        #     自定义类print函数, 借用c语言
        #     printf
        #     Mypstr：是待显示的字符串
        # ###
        self.textBrowser.append(mypstr)  # 在指定的区域显示提示信息
        self.cursor = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursor.End)  # 光标移到最后，这样就会自动显示出来
        QtWidgets.QApplication.processEvents()  # 一定加上这个功能，不然有卡顿

    def on_pushButton_clicked(self):#槽函数
        print("OK")
        print("Please tell me the command(请在5秒之内说出识别的语音):")
        str="Please tell me the command(请在5秒之内说出识别的语音):"
        # self.textBrowser.setText(str)
        self.printf(str)
        self.audio_record(AUDIO_OUTPUT, 5)  # 设置录音的时间s


        asr_result = self.aip_get_asrresult(client, AUDIO_OUTPUT, AUDIO_FORMAT)
        if len(asr_result) != 0:  # 如果有语音
            print("Identify Result:", asr_result[0])#打印识别结果
            self.printf("Identify Result:"+asr_result[0])
            self.printf("End")
            print("Start Control...")
            #进行控制
            print("Control End...")
            # if asr_result[0].find("退出") != -1:
            #     break;
            time.sleep(1)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # 调用百度语音API
    APPID = "24908798"
    API_KEY = "klNu9LbzhSGEoNojXLdw6YTE"
    SECRET_KEY = "6HsMVGSgsu0q73NwORoyGlfe8qz3hSDf"

    DEV_PID = "1536"  # 1536,普通话(支持简单的英文识别),搜索模型,无标点,支持自定义词库
    AUDIO_FORMAT = "WAV"
    AUDIO_OUTPUT = "audio_output.wav"

    # 新建AipSpeech
    client = AipSpeech(APPID, API_KEY, SECRET_KEY)
    CUID = get_mac_address()
    mainwindow = QMainWindow()
    dlg = Ui_MainWindow()
    dlg.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())