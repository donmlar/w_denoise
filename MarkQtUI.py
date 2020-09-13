# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal ,QThread
from PyQt5.QtGui import QPixmap
import sys
import pb_use_m
import view_img
from PyQt5.QtGui import QTextCursor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1329, 736)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.start_denoise = QtWidgets.QPushButton(self.centralwidget)
        self.start_denoise.setGeometry(QtCore.QRect(479, 519, 81, 31))
        self.start_denoise.setObjectName("start_denoise")
        self.get_input_dng = QtWidgets.QPushButton(self.centralwidget)
        self.get_input_dng.setGeometry(QtCore.QRect(20, 40, 111, 31))
        self.get_input_dng.setObjectName("get_input_dng")
        self.set_output_path = QtWidgets.QPushButton(self.centralwidget)
        self.set_output_path.setGeometry(QtCore.QRect(20, 110, 111, 31))
        self.set_output_path.setObjectName("set_output_path")
        self.output_path_viewer = QtWidgets.QTextBrowser(self.centralwidget)
        self.output_path_viewer.setGeometry(QtCore.QRect(140, 110, 421, 41))
        self.output_path_viewer.setObjectName("output_path_viewer")
        self.input_path_viewer = QtWidgets.QTextBrowser(self.centralwidget)
        self.input_path_viewer.setGeometry(QtCore.QRect(140, 40, 421, 41))
        self.input_path_viewer.setObjectName("input_path_viewer")
        self.light_slider = QtWidgets.QSlider(self.centralwidget)
        self.light_slider.setGeometry(QtCore.QRect(150, 180, 181, 16))
        self.light_slider.setMaximum(40)
        self.light_slider.setSingleStep(1)
        self.light_slider.setPageStep(2)
        self.light_slider.setOrientation(QtCore.Qt.Horizontal)
        self.light_slider.setObjectName("light_slider")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 180, 54, 21))
        self.label.setObjectName("label")
        self.rate_slider = QtWidgets.QSlider(self.centralwidget)
        self.rate_slider.setGeometry(QtCore.QRect(150, 230, 181, 16))
        self.rate_slider.setMinimum(-10)
        self.rate_slider.setMaximum(10)
        self.rate_slider.setPageStep(1)
        self.rate_slider.setProperty("value", 0)
        self.rate_slider.setOrientation(QtCore.Qt.Horizontal)
        self.rate_slider.setObjectName("rate_slider")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 230, 71, 21))
        self.label_2.setObjectName("label_2")
        self.gamme_slider = QtWidgets.QSlider(self.centralwidget)
        self.gamme_slider.setGeometry(QtCore.QRect(150, 280, 181, 16))
        self.gamme_slider.setOrientation(QtCore.Qt.Horizontal)
        self.gamme_slider.setObjectName("gamme_slider")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 280, 71, 21))
        self.label_3.setObjectName("label_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(40, 560, 531, 121))
        self.textBrowser.setObjectName("textBrowser")
        self.light_label = QtWidgets.QLabel(self.centralwidget)
        self.light_label.setGeometry(QtCore.QRect(350, 180, 54, 12))
        self.light_label.setObjectName("light_label")
        self.rate_lable = QtWidgets.QLabel(self.centralwidget)
        self.rate_lable.setGeometry(QtCore.QRect(350, 230, 54, 12))
        self.rate_lable.setObjectName("rate_lable")
        self.image_lable = QtWidgets.QLabel(self.centralwidget)
        self.image_lable.setGeometry(QtCore.QRect(610, 40, 621, 571))
        self.image_lable.setObjectName("image_lable")
        self.get_view = QtWidgets.QPushButton(self.centralwidget)
        self.get_view.setGeometry(QtCore.QRect(359, 519, 91, 31))
        self.get_view.setObjectName("get_view")
        self.blue_gain_slider = QtWidgets.QSlider(self.centralwidget)
        self.blue_gain_slider.setGeometry(QtCore.QRect(150, 330, 181, 16))
        self.blue_gain_slider.setMinimum(-99)
        self.blue_gain_slider.setOrientation(QtCore.Qt.Horizontal)
        self.blue_gain_slider.setObjectName("blue_gain_slider")
        self.green_gain_slider = QtWidgets.QSlider(self.centralwidget)
        self.green_gain_slider.setGeometry(QtCore.QRect(150, 380, 181, 16))
        self.green_gain_slider.setMinimum(-99)
        self.green_gain_slider.setOrientation(QtCore.Qt.Horizontal)
        self.green_gain_slider.setObjectName("green_gain_slider")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 320, 54, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 370, 54, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(120, 320, 21, 31))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(110, 370, 31, 31))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(340, 370, 21, 31))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(340, 320, 21, 31))
        self.label_9.setObjectName("label_9")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(60, 470, 73, 31))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(160, 470, 73, 31))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_CPU = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_CPU.setGeometry(QtCore.QRect(60, 500, 101, 41))
        self.checkBox_CPU.setObjectName("checkBox_CPU")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(110, 420, 31, 31))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(40, 420, 54, 31))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(340, 420, 21, 31))
        self.label_12.setObjectName("label_12")
        self.purple_drift_slider = QtWidgets.QSlider(self.centralwidget)
        self.purple_drift_slider.setGeometry(QtCore.QRect(150, 430, 181, 16))
        self.purple_drift_slider.setMinimum(-99)
        self.purple_drift_slider.setOrientation(QtCore.Qt.Horizontal)
        self.purple_drift_slider.setObjectName("purple_drift_slider")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1329, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "一个raw降噪工具 by s3"))
        self.start_denoise.setText(_translate("MainWindow", "开始处理"))
        self.get_input_dng.setText(_translate("MainWindow", "选择图像文件"))
        self.set_output_path.setText(_translate("MainWindow", "设置输出目录"))
        self.get_view.setText(_translate("MainWindow", "亮度浏览"))
        self.label.setText(_translate("MainWindow", "亮度"))
        self.label_2.setText(_translate("MainWindow", "比例控制"))
        self.label_3.setText(_translate("MainWindow", "暗部优化"))
        self.light_label.setText(_translate("MainWindow", "0.0"))
        self.rate_lable.setText(_translate("MainWindow", "0.0"))
        self.label_4.setText(_translate("MainWindow", "色温1"))
        self.label_5.setText(_translate("MainWindow", "色温2"))
        self.label_6.setText(_translate("MainWindow", "黄"))
        self.label_7.setText(_translate("MainWindow", "品红"))
        self.label_8.setText(_translate("MainWindow", "绿"))
        self.label_9.setText(_translate("MainWindow", "蓝"))
        self.checkBox.setText(_translate("MainWindow", "soft"))
        self.checkBox_2.setText(_translate("MainWindow", "mix"))
        self.checkBox_CPU.setText(_translate("MainWindow", "CPU模式"))
        self.label_10.setText(_translate("MainWindow", "紫"))
        self.label_11.setText(_translate("MainWindow", "偏移"))
        self.label_12.setText(_translate("MainWindow", "黄"))


        self.get_input_dng.clicked.connect(lambda: self.getDngFile())
        self.set_output_path.clicked.connect(lambda: self.serOutputPath())
        self.start_denoise.clicked.connect(lambda: self.process())


        self.light_slider.valueChanged[int].connect(self.updateLightLable)
        self.rate_slider.valueChanged[int].connect(self.updateRateLable)





        self.get_view.clicked.connect(self.updateView)

        sys.stdout = Stream(newText=self.onUpdateText)


    # 更新控制台
    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()


    # 更新滑块标签
    def updateLightLable(self,value):
        self.light_label.setText(str(value/10))
    def updateRateLable(self,value):
        self.rate_lable.setText(str(value/10))


    def getDngFile(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "打开raw文件", '.', "RAW文件(*.dng *.nef *.rw2 *.cr2 *.cr3 *.arw *.raf)")
        print(fileName)
        # print('输入文件：'+dir)

        self.input_path_viewer.setText(fileName)



    def serOutputPath(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(None, "Open Directory",'.',QtWidgets.QFileDialog.ShowDirsOnly)
        print(dir)

        self.output_path_viewer.setText(dir)
        # print('设定输出目录：'+dir)






    def process(self):
        fileName = self.input_path_viewer.toPlainText()
        output_path = self.output_path_viewer.toPlainText()


        # pb_use.restore_mode_pb_single(pb_path,fileName)
        light = self.light_slider.value()/10
        rate = self.rate_slider.value()
        gamma = self.gamme_slider.value()/100
        #
        # th = threading.Thread(target=pb_use.restore_mode_pb_single, args=(pb_path,fileName ,output_path,light,rate,gamma))
        # th.start()
        #
        blue_gain = self.blue_gain_slider.value()/200
        green_gain = self.green_gain_slider.value()/200

        purple_drift = self.purple_drift_slider.value()

        soft = self.checkBox.isChecked()
        mix = self.checkBox_2.isChecked()
        type = 1
        if soft:
            type = 2
        if mix:
            type = 3

        cpu_only = self.checkBox_CPU.isChecked()

        dict = {}
        dict['fileName'] = fileName
        dict['output_path'] = output_path
        dict['light'] = light
        dict['rate'] = rate
        dict['gamma'] = gamma
        dict['blue_gain'] = blue_gain
        dict['green_gain'] = green_gain
        dict['type'] = type
        dict['cpu_only'] = cpu_only
        dict['purple_drift'] = purple_drift

        self.start_denoise.setText("处理中")
        self.start_denoise.setEnabled(False)
        self.get_view.setEnabled(False)

        self.thread = ProcessImg(dict)
        self.thread.signal.connect(self.processFinish)
        self.thread.start()


    def processFinish(self):

        self.start_denoise.setText("开始处理")
        self.start_denoise.setEnabled(True)
        self.get_view.setEnabled(True)




    def updateView(self):
        fileName = self.input_path_viewer.toPlainText()
        output_path = self.output_path_viewer.toPlainText()

        pb_path = './pb_model/n3/frozen_model.pb'
        # pb_use.restore_mode_pb_single(pb_path,fileName)
        light = self.light_slider.value()/10
        rate = self.rate_slider.value()
        gamma = self.gamme_slider.value()/100

        blue_gain = self.blue_gain_slider.value()/200
        green_gain = self.green_gain_slider.value()/200
        purple_drift = self.purple_drift_slider.value()
        cpu_only = self.checkBox_CPU.isChecked()

        dict = {}
        dict['pb_path'] = pb_path
        dict['fileName'] = fileName
        dict['light'] = light
        dict['rate'] = rate
        dict['gamma'] = gamma
        dict['blue_gain'] = blue_gain
        dict['green_gain'] = green_gain
        dict['cpu_only'] = cpu_only
        dict['purple_drift'] = purple_drift

        self.thread = ProcessView(dict)
        self.thread.signal2.connect(self.viewFinish)
        self.thread.start()

        self.start_denoise.setEnabled(False)
        self.get_view.setEnabled(False)

    def viewFinish(self):
        # self.image_lable.setPixmap(QPixmap.fromImage(img))

        fileName = self.input_path_viewer.toPlainText()

        name = fileName.split('/')[-1].split('.')[0]

        pixmap = QPixmap("./tmp/"+name+"_v.png")

        self.image_lable.setPixmap(pixmap)
        # self.resize(self.image.width(), self.image.height())

        self.image_lable.repaint()
        self.image_lable.setScaledContents(True)


        self.start_denoise.setEnabled(True)
        self.get_view.setEnabled(True)



    # 更新控制台
class Stream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))




class ProcessImg(QThread):
    signal = pyqtSignal()  # 括号里填写信号传递的参数
    def __init__(self,dict):
        super().__init__()
        self.dict =dict



    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        self.dict['t'] = 123
        # pb_use.restore_mode_pb_single(self.pb_path,self.fileName ,self.output_path,self.light,self.rate,self.gamma)
        th = pb_use_m.restore_mult_model(self.dict)

        # th = pb_use.restore_mode_pb_single(self.dict)
        th.start()

        while th.isAlive():
            self.sleep(1)
        self.signal.emit()  # 发射信号


class ProcessView(QThread):
    signal2 = pyqtSignal()  # 括号里填写信号传递的参数
    def __init__(self,dict):
        super().__init__()
        self.dict =dict



    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作



        th = view_img.ViewThread(self.dict)
        th.start()


        while th.isAlive():
            self.sleep(1)
        self.signal2.emit()  # 发射信号
