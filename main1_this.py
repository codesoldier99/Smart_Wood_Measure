import os
import shutil
import sys
import threading
import time
# import numpngw
import cv2
import numpy as np
import pandas as pd
from PyQt5 import Qt, QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QApplication, QMainWindow, QWidget, QFileDialog, QTableWidgetItem, \
    QAbstractItemView, QHeaderView

from UI_Camera import Ui_MainWindow
from Child_UI import Ui_Form
import pyzed.sl as sl
import camera_control
import depth_cv_mix
import depth_cv_elli_singlePic
import depth_cv_elli_singlePic_back
# from qt_material import apply_stylesheet

name_dir = ""
name2_dir = ""
class uic(QMainWindow, Ui_MainWindow):
    conn = pyqtSignal(str) #声明一个带str类型参数的信号

    def __init__(self, parent=None):
        super(uic, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.capture)
        self.pushButton_2.clicked.connect(self.capture2)   #增加一个函数
        self.label.setScaledContents(True)
        self.label_2.setScaledContents(True)
        self.init = sl.InitParameters()
        self.init.camera_resolution = sl.RESOLUTION.HD2K  # 将摄像头分辨率设为2K
        self.init.camera_fps = 15  # Set fps at 15帧数率为30fps
        self.init.depth_mode=sl.DEPTH_MODE.ULTRA
        self.init.coordinate_units = sl.UNIT.METER
        # self.init.depth_maximum_distance=2
        # self.init.depth_minimum_distance=0.4
        self.cam = None
        # triggered的作用类似于button中的clicked，起到触发事件的作用
        self.action_19.triggered.connect(self.liangdu)
        self.action_20.triggered.connect(self.duibidu)
        self.action_21.triggered.connect(self.sediao)
        self.action_22.triggered.connect(self.baohedu)
        self.action_23.triggered.connect(self.baoguang)
        self.action_24.triggered.connect(self.ruidu)
        self.action_25.triggered.connect(self.baipingheng)


        # python Thread类表示在单独的控制线程中运行的活动
        th = threading.Thread(target=self.main)
        th.start()
        self.ld = False
        self.dbd = False
        self.sd = False
        self.bhd = False
        self.re = False
        self.bg = False
        self.bph = False
        # self.rs = False
        self.cap = False
        self.conn.connect(self.handle_img2)
        self.conn.connect(self.handle_img)
        self.stopEvent = threading.Event()
        self.stopEvent.clear()
        self.pushButton_3.clicked.connect(self.stopEvent.set)
        # self.pushButton_4.clicked.connect(self.caiji_calculate)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1199, 647)
        MainWindow.setFixedSize(1199, 647)
        MainWindow.setStyleSheet("QPushButton\n"
                                 "{\n"
                                 "background-color: rgb(225, 225, 225);\n"
                                 "border:2px groove gray;\n"
                                 "border-radius:10px;\n"
                                 "padding:2px 4px;\n"
                                 "border-style: outset;\n"
                                 "}\n"
                                 "QPushButton:hover\n"
                                 "{\n"
                                 "background-color:rgb(229, 241, 251);\n"
                                 "color: black;\n"
                                 "}\n"
                                 "QPushButton:pressed\n"
                                 "{\n"
                                 "background-color:rgb(0, 0, 0);\n"
                                 "border-style: inset;\n"
                                 "}\n"
                                 "QMenu{\n"
                                 "   background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #00ffff, stop:0.5 #505050, stop:0.98 #00ffff);\n"
                                 "   border:0px;\n"
                                 "   border-radius:4px;\n"
                                 "   color:white;\n"
                                 "}\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(11, 555, 1141, 51))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pic/pai.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("pic/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_3.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("pic/Hint.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_4.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("pic/g1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(60, 40, 1091, 481))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(500, 500))
        self.label.setStyleSheet("border-image: url(:/newPrefix/pic/g1.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QtCore.QSize(500, 500))
        self.label_2.setStyleSheet("border-image: url(:/newPrefix/pic/wallhaven-rd9q77.jpg);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(380, 630, 241, 31))
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(630, 630, 151, 31))
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1199, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuBar.sizePolicy().hasHeightForWidth())
        self.menuBar.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.menuBar.setFont(font)
        self.menuBar.setStyleSheet("QMenuBar{\n"
                                   "   background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #00ffff, stop:0.5 #505050, stop:0.98 #00ffff);\n"
                                   "   border:0px;\n"
                                   "   border-radius:4px;\n"
                                   "   color:white;\n"
                                   "}")
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.menu.setFont(font)
        self.menu.setStyleSheet("")
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menuBar)
        self.actionliangdu = QtWidgets.QAction(MainWindow)
        self.actionliangdu.setObjectName("actionliangdu")
        self.action_10 = QtWidgets.QAction(MainWindow)
        self.action_10.setObjectName("action_10")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.action_6 = QtWidgets.QAction(MainWindow)
        self.action_6.setObjectName("action_6")
        self.action_7 = QtWidgets.QAction(MainWindow)
        self.action_7.setObjectName("action_7")
        self.action_8 = QtWidgets.QAction(MainWindow)
        self.action_8.setObjectName("action_8")
        self.action_11 = QtWidgets.QAction(MainWindow)
        self.action_11.setObjectName("action_11")
        self.action_19 = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.action_19.setFont(font)
        self.action_19.setObjectName("action_19")
        self.action_20 = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.action_20.setFont(font)
        self.action_20.setObjectName("action_20")
        self.action_21 = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.action_21.setFont(font)
        self.action_21.setObjectName("action_21")
        self.action_22 = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.action_22.setFont(font)
        self.action_22.setObjectName("action_22")
        self.action_23 = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.action_23.setFont(font)
        self.action_23.setObjectName("action_23")
        self.action_24 = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.action_24.setFont(font)
        self.action_24.setObjectName("action_24")
        self.action_25 = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.action_25.setFont(font)
        self.action_25.setObjectName("action_25")
        self.menu.addAction(self.action_19)
        self.menu.addAction(self.action_20)
        self.menu.addAction(self.action_21)
        self.menu.addAction(self.action_22)
        self.menu.addAction(self.action_23)
        self.menu.addAction(self.action_24)
        self.menu.addAction(self.action_25)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "图像采集"))
        self.pushButton.setText(_translate("MainWindow", "拍车尾"))
        self.pushButton_2.setText(_translate("MainWindow", "拍车头"))
        self.pushButton_3.setText(_translate("MainWindow", "关闭"))
        self.pushButton_4.setText(_translate("MainWindow", "材积计算"))
        self.label_3.setText(_translate("MainWindow", "请输入检尺长度："))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "检尺长"))
        self.menu.setTitle(_translate("MainWindow", "参数调整"))
        self.menu_2.setTitle(_translate("MainWindow", "帮助"))
        self.actionliangdu.setText(_translate("MainWindow", "liangdu"))
        self.action_10.setText(_translate("MainWindow", "亮度"))
        self.action_3.setText(_translate("MainWindow", "对比度"))
        self.action_4.setText(_translate("MainWindow", "色调"))
        self.action_5.setText(_translate("MainWindow", "饱和度"))
        self.action_6.setText(_translate("MainWindow", "锐度"))
        self.action_7.setText(_translate("MainWindow", "曝光时间"))
        self.action_8.setText(_translate("MainWindow", "白平衡和温度"))
        self.action_11.setText(_translate("MainWindow", "亮度"))
        self.action_19.setText(_translate("MainWindow", "亮度"))
        self.action_20.setText(_translate("MainWindow", "对比度"))
        self.action_21.setText(_translate("MainWindow", "色调"))
        self.action_22.setText(_translate("MainWindow", "饱和度"))
        self.action_23.setText(_translate("MainWindow", "锐度"))
        self.action_24.setText(_translate("MainWindow", "曝光时间"))
        self.action_25.setText(_translate("MainWindow", "白平衡和温度"))
    def handle_img2(self, i):
        if i == "0":
            self.label.setPixmap(QPixmap(""))

        if i == "1":
            self.label.setPixmap(QPixmap("ZED1.png"))
            #self.label.setPixmap(QPixmap(""))
        # if i == "2":
        #     try:
        #         self.label_2.setPixmap(QPixmap("ZED1.png"))
        #
        #         name = "pic/" + time.strftime("%Y%m%d%H%M%S") + ".png"
        #         name2 = "pic/depth" + time.strftime("%Y%m%d%H%M%S") + ".png"
        #         self.label_2.pixmap().save(name)
        #         print(name)
        #         # img = cv2.imread("ZED1.jpg")
        #         time.sleep(0.3)
        #
        #         shutil.copyfile("ZED2.png", name2)
        #         global name_dir
        #         name_dir = "/home/zsw/mmdetection-2.19.1/Qt-Camera2/" + name
        #         # print(name_dir)
        #         global name2_dir
        #         name2_dir = "/home/zsw/mmdetection-2.19.1/Qt-Camera2/" + name2
        #         # cv2.imwrite(img,name)
        #         # time.sleep(0.3)
        #         # shutil.copyfile("ZED1.jpg", name)
        #
        #         # depth_cv_mix.inference(depth_pic_path=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\depth\depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
        #         # depth_cv_mix.inference(depth_pic_path="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/depth/depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
        #         # 拍车尾
        #         depth_cv_mix.inferenceTou(depth_pic_path=name2_dir, input_dir=name_dir)
        #
        #     except Exception as e:
        #         print(e)
    def handle_img(self, i):
        if i == "0":
            self.label.setPixmap(QPixmap(""))

        if i == "1":
            #self.label.setPixmap(QPixmap(""))
            self.label.setPixmap(QPixmap("ZED1.png"))

        # if i == "2":
        #     try:
        #         self.label_2.setPixmap(QPixmap("ZED1.png"))
        #
        #         name = "pic/" + time.strftime("%Y%m%d%H%M%S") + ".png"
        #         name2 = "pic/depth" + time.strftime("%Y%m%d%H%M%S") + ".png"
        #         self.label_2.pixmap().save(name)
        #         print(name)
        #         # img = cv2.imread("ZED1.jpg")
        #         time.sleep(0.3)
        #
        #         shutil.copyfile("ZED2.png", name2)
        #         global name_dir
        #         name_dir = "/home/zsw/mmdetection-2.19.1/Qt-Camera2/" + name
        #         # print(name_dir)
        #         global name2_dir
        #         name2_dir = "/home/zsw/mmdetection-2.19.1/Qt-Camera2/" + name2
        #         # cv2.imwrite(img,name)
        #         # time.sleep(0.3)
        #         # shutil.copyfile("ZED1.jpg", name)
        #
        #         # depth_cv_mix.inference(depth_pic_path=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\depth\depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
        #         # depth_cv_mix.inference(depth_pic_path="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/depth/depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
        #         # 拍车尾
        #         depth_cv_mix.inferenceBACK(depth_pic_path=name2_dir, input_dir=name_dir)
        #
        #     except Exception as e:
        #         print(e)

    def liangdu(self):#设置亮度
        self.ld = True
        #self.main()
    def duibidu(self):#设置对比度
        self.dbd = True
    def sediao(self):#设置色调
        self.sd = True
    def baohedu(self):#设置饱和度
        self.bhd = True
    def ruidu(self):#设置锐度
        self.re = True
    def baoguang(self):#设置曝光
        self.bg = True
    def baipingheng(self):#设置白平衡
        self.bph = True
    # def reset(self):#重置
    #     self.rs = True
    def capture2(self):  # 拍车头
        try:
            self.label_2.setPixmap(QPixmap("ZED1.png"))

            name = "pic/" + time.strftime("%Y%m%d%H%M%S") + ".png"
            name2 = "pic/depth" + time.strftime("%Y%m%d%H%M%S") + ".png"
            self.label_2.pixmap().save(name)
            print(name)
            # img = cv2.imread("ZED1.jpg")
            time.sleep(0.3)

            shutil.copyfile("ZED2.png", name2)
            global name_dir
            name_dir = "C:/backup2022_12_5/backup2022_12_5/Qt-Camera/" + name
            # print(name_dir)
            global name2_dir
            name2_dir = "C:/backup2022_12_5/backup2022_12_5/Qt-Camera/" + name2
            # cv2.imwrite(img,name)
            # time.sleep(0.3)
            # shutil.copyfile("ZED1.jpg", name)

            # depth_cv_mix.inference(depth_pic_path=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\depth\depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
            # depth_cv_mix.inference(depth_pic_path="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/depth/depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
            # 拍车尾
            r =  depth_cv_elli_singlePic_back.inference_wood(depth_pic_path=name2_dir, input_dir=name_dir)
            self.label_2.setPixmap(QPixmap(r))
        except Exception as e:
            print(e)
    def capture(self):#拍车尾
        try:
            self.label_2.setPixmap(QPixmap("ZED1.png"))
            name = "pic/" + time.strftime("%Y%m%d%H%M%S") + ".png"
            name2 = "pic/depth" + time.strftime("%Y%m%d%H%M%S") + ".png"
            self.label_2.pixmap().save(name)
            print(name)
            # img = cv2.imread("ZED1.jpg    )
            time.sleep(0.3)
            shutil.copyfile("ZED2.png", name2)
            global name_dir
            name_dir = "C:/backup2022_12_5/backup2022_12_5/Qt-Camera/" + name
            # print(name_dir)
            global name2_dir
            name2_dir = "C:/backup2022_12_5/backup2022_12_5/Qt-Camera/" + name2
            # cv2.imwrite(img,name)
            # time.sleep(0.3)
            # shutil.copyfile("ZED1.jpg", name)

            # depth_cv_mix.inference(depth_pic_path=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\depth\depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
            # depth_cv_mix.inference(depth_pic_path="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/depth/depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
            # 拍车尾
            r = depth_cv_elli_singlePic.inference_wood(depth_pic_path=name2_dir, input_dir=name_dir)
            self.label_2.setPixmap(QPixmap(r))

        except Exception as e:
            print(e)


    # def caiji_calculate(self):
    #     global cam,runtime,mat
    #     dep_path = camera_control.depth(cam, runtime, mat, flag=True)
    #     depth_cv_mix.inference(dep_path, r"E:\zed_pic\longdu_1-7")  # 读取图片进行处理

    # 输出相机信息
    def print_camera_information(self, cam):
        print("Resolution: {0}, {1}.".format(round(cam.get_camera_information().camera_resolution.width, 2),
                                             cam.get_camera_information().camera_resolution.height))
        print("Camera FPS: {0}.".format(cam.get_camera_information().camera_fps))
        print("Firmware: {0}.".format(cam.get_camera_information().camera_firmware_version))
        print("Serial number: {0}.\n".format(cam.get_camera_information().serial_number))
    def main(self):
        try:
            print("Running...")
            # cam = sl.Camera()
            init = sl.InitParameters()
            init.camera_resolution = sl.RESOLUTION.HD2K  # 将摄像头分辨率设为2K
            init.camera_fps = 15  # Set fps at 15帧数率为30fps
            self.cam = sl.Camera()

            if not self.cam.is_opened():
                print("Opening ZED Camera...")
            status = self.cam.open(init)
            if status != sl.ERROR_CODE.SUCCESS:
                print(repr(status))
                exit()

            runtime = sl.RuntimeParameters()
            # runtime.sensing_mode = sl.SENSING_MODE.FILL  # Use FILL sensing mode 使用填充传感模式
            # Setting the depth confidence parameters设置深度置信参数
            runtime.confidence_threshold = 100
            runtime.textureness_confidence_threshold = 100
            mat = sl.Mat()
            self.print_camera_information(self.cam)
            #self.print_help()
            key = ''

            while key != 113:  # for 'q' key
                start = time.time()
                if self.ld:
                    self.cam.set_camera_settings(sl.VIDEO_SETTINGS.BRIGHTNESS, 0)
                    #self.switch_camera_settings()
                    self.ld = False
                    print("设置亮度")
                if self.dbd:
                    self.cam.set_camera_settings(sl.VIDEO_SETTINGS.CONTRAST, 0)
                    print("设置对比度")
                    self.dbd = False
                if self.sd:
                    self.cam.set_camera_settings(sl.VIDEO_SETTINGS.HUE, 0)
                    print("设置色调")
                    self.sd = False
                if self.bhd:
                    self.cam.set_camera_settings(sl.VIDEO_SETTINGS.SATURATION, 0)
                    print("设置饱和度")
                    self.bhd = False
                if self.re:
                    self.cam.set_camera_settings(sl.VIDEO_SETTINGS.SHARPNESS, 0)
                    print("设置锐度")
                    self.re = False
                if self.bg:
                    self.cam.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, 0)
                    print("设置曝光")
                    self.bg = False
                if self.bph:
                    self.cam.set_camera_settings(sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE, 0)
                    print("设置白平衡")
                    self.bph = False
                # if self.rs:
                #     self.cam.set_camera_settings(sl.VIDEO_SETTINGS.BRIGHTNESS, -1)  # 亮度
                #     self.cam.set_camera_settings(sl.VIDEO_SETTINGS.CONTRAST, -1)  # 对比度
                #     self.cam.set_camera_settings(sl.VIDEO_SETTINGS.HUE, -1)  # 色调
                #     self.cam.set_camera_settings(sl.VIDEO_SETTINGS.SATURATION, -1)  # 饱和度
                #     self.cam.set_camera_settings(sl.VIDEO_SETTINGS.SHARPNESS, -1)  # 锐度
                #     self.cam.set_camera_settings(sl.VIDEO_SETTINGS.GAIN, -1)  #
                #     self.cam.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, -1)  # 曝光时间
                #     self.cam.set_camera_settings(sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE, -1)  # 白平衡和温度
                #     self.rs = False
                #     print("Camera settings: reset")

                err = self.cam.grab(runtime)
                #cv2.namedWindow('ZED1', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
                # cv2.namedWindow('ZED2', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
                # cv2.namedWindow('ZED2', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
                if err == sl.ERROR_CODE.SUCCESS:
                    #左目图像
                    self.cam.retrieve_image(mat, sl.VIEW.LEFT)

                    cv2.imwrite("ZED1.png", mat.get_data())
                    # mat.write("ZED1.png")
                    # mat.write("ZED1.png")

                    # self.cam.retrieve_image(mat, sl.VIEW.DEPTH)
                    self.cam.retrieve_measure(mat, sl.MEASURE.DEPTH)

                    mat.write("ZED2.png")
                    # cv2.imwrite("ZED2.png", mat.get_data(),[int(cv2.IMWRITE_PNG_COMPRESSION),3])
                    # numpngw.write_png("ZED2.png", mat)
                    self.conn.emit("1")

                    if self.cap:
                        self.conn.emit("2")
                        self.cap = False
                        # print(name_dir)
                        # depth_cv_mix.inference("E:\zed_pic\longdu_1-7/fill/20220107depth.jpg", r"E:\zed_pic\longdu_1-7")
                        # depth_cv_mix.inference(name_dir,name2_dir)
                    end = time.time()
                    # dep_path = camera_control.depth(self.cam, runtime, mat)
                    # depth_cv_mix.inference(dep_path, r"E:\zed_pic\longdu_1-7")  # 读取图片进行处理
                    # depth_cv_mix.inference("E:\zed_pic\longdu_1-7/fill/20220107depth.jpg", r"E:\zed_pic\longdu_1-7")
                    strtime = '%.5f s' % (end - start)

                if self.stopEvent.is_set():
                    self.conn.emit("0")
                    break
            # dep_path = camera_control.depth(self.cam, runtime, mat)
            # depth_cv_mix.inference("E:\zed_pic\longdu_1-7/fill/20220107depth.jpg", r"E:\zed_pic\longdu_1-7")  # 读取图片进行处理
            cv2.destroyAllWindows()
            self.cam.close()
            print("\nFINISH")
        except Exception as e:
            print(e)
    def switch_camera_settings(self):
        global camera_settings
        global str_camera_settings
        if camera_settings == sl.VIDEO_SETTINGS.BRIGHTNESS:
            camera_settings = sl.VIDEO_SETTINGS.CONTRAST
            str_camera_settings = "Contrast"
            print("Camera settings: CONTRAST")
        elif camera_settings == sl.VIDEO_SETTINGS.CONTRAST:
            camera_settings = sl.VIDEO_SETTINGS.HUE
            str_camera_settings = "Hue"
            print("Camera settings: HUE")
        elif camera_settings == sl.VIDEO_SETTINGS.HUE:
            camera_settings = sl.VIDEO_SETTINGS.SATURATION
            str_camera_settings = "Saturation"
            print("Camera settings: SATURATION")
        elif camera_settings == sl.VIDEO_SETTINGS.SATURATION:
            camera_settings = sl.VIDEO_SETTINGS.SHARPNESS
            str_camera_settings = "Sharpness"
            print("Camera settings: Sharpness")
        elif camera_settings == sl.VIDEO_SETTINGS.SHARPNESS:
            camera_settings = sl.VIDEO_SETTINGS.GAIN
            str_camera_settings = "Gain"
            print("Camera settings: GAIN")
        elif camera_settings == sl.VIDEO_SETTINGS.GAIN:
            camera_settings = sl.VIDEO_SETTINGS.EXPOSURE
            str_camera_settings = "Exposure"
            print("Camera settings: EXPOSURE")
        elif camera_settings == sl.VIDEO_SETTINGS.EXPOSURE:
            camera_settings = sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE
            str_camera_settings = "White Balance"
            print("Camera settings: WHITEBALANCE")
        elif camera_settings == sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE:
            camera_settings = sl.VIDEO_SETTINGS.BRIGHTNESS
            str_camera_settings = "Brightness"
            print("Camera settings: BRIGHTNESS")

class Ui_ChildWindow(QMainWindow):

    def __init__(self):
        super(QtWidgets.QMainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.path = ""

        self.dirpath = "C:/result/2025"

        self.flist = []
        for f in os.listdir(self.dirpath):
            path_file = os.path.join(self.dirpath, f)
            if self.get_FileCreateTime(path_file):
                self.flist.append(f)
                print(f)

        for f in self.flist:
            self.tableWidget_2.insertRow(0)
            self.tableWidget_2.setItem(0, 0, QTableWidgetItem(str(f)))
            self.tableWidget_2.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    def get_FileCreateTime(self,filePath):
        # '''获取文件的创建时间'''
        # filePath = unicode(filePath,'utf8')
        t = os.path.getctime(filePath)
        # return TimeStampToTime(t)
        return time.time() - t < 86400 * 2

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1385, 497)
        MainWindow.setStyleSheet("QPushButton\n"
                           "{\n"
                           "background-color: rgb(225, 225, 225);\n"
                           "border:2px groove gray;\n"
                           "border-radius:10px;\n"
                           "padding:2px 4px;\n"
                           "border-style: outset;\n"
                           "}\n"
                           "QPushButton:hover\n"
                           "{\n"
                           "background-color:rgb(229, 241, 251);\n"
                           "color: black;\n"
                           "}\n"
                           "QPushButton:pressed\n"
                           "{\n"
                           "background-color:rgb(0, 0, 0);\n"
                           "border-style: inset;\n"
                           "}")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.retranslateUi(MainWindow)

        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 90, 813, 371))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setStyleSheet("selection-background-color:pink")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.raise_()

        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(816, 90, 501, 371))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        # 标题
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setHorizontalHeaderLabels(['文件名'])
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(90, 10, 200, 80))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setIconSize(QtCore.QSize(18, 18))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("打开文件")
        MainWindow.setCentralWidget(self.centralWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.openfile)
        self.pushButton.clicked.connect(self.creat_table_show)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "检尺信息汇总表"))

    def openfile(self):

        ###获取路径===================================================================

        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '/home/zsw/Desktop/result', 'Excel files(*.xlsx , *.xls)')
        self.path = openfile_name[0]
        #print(openfile_name)
        # global path_openfile_name


        ###获取路径====================================================================

        # path_openfile_name = openfile_name[0]


    def creat_table_show(self):
        try:
        ###===========读取表格，转换表格，===========================================
            if len(self.path) > 0:
                input_table = pd.read_excel(self.path,sheet_name=1)
            #print(input_table)
                input_table_rows = input_table.shape[0]
                input_table_colunms = input_table.shape[1]
            #print(input_table_rows)
            #print(input_table_colunms)
                input_table_header = input_table.columns.values.tolist()
            #print(input_table_header)

            ###===========读取表格，转换表格，============================================
            ###======================给tablewidget设置行列表头============================

                self.tableWidget.setColumnCount(input_table_colunms)
                self.tableWidget.setRowCount(input_table_rows)
                self.tableWidget.setHorizontalHeaderLabels(input_table_header)

            ###======================给tablewidget设置行列表头============================

            ###================遍历表格每个元素，同时添加到tablewidget中========================
                for i in range(input_table_rows):
                    input_table_rows_values = input_table.iloc[[i]]
                    #print(input_table_rows_values)
                    input_table_rows_values_array = np.array(input_table_rows_values)
                    input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                #print(input_table_rows_values_list)
                    for j in range(input_table_colunms):
                        input_table_items_list = input_table_rows_values_list[j]
                    #print(input_table_items_list)
                    # print(type(input_table_items_list))

            ###==============将遍历的元素添加到tablewidget中并显示=======================

                        input_table_items = str(input_table_items_list)
                        newItem = QTableWidgetItem(input_table_items)
                        newItem.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                        self.tableWidget.setItem(i, j, newItem)

            ###================遍历表格每个元素，同时添加到tablewidget中========================
            else:
                self.centralWidget.show()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = uic()
    child = Ui_ChildWindow()
    btn = ui.pushButton_4
    btn.clicked.connect(child.show)
    child.show()
    ui.show()
    # apply_stylesheet(app, theme='dark_teal.xml')
    sys.exit(app.exec_())