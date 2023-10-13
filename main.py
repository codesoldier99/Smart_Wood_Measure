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
from PyQt5.QtWidgets import QFrame, QApplication, QMainWindow, QWidget, QFileDialog, QTableWidgetItem, QAbstractItemView

from UI_Camera import Ui_MainWindow
from Child_UI import Ui_Form
import pyzed.sl as sl
import camera_control
import depth_cv_mix
import depth_cv_elli_singlePic

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
        self.conn.connect(self.handle_img)
        self.stopEvent = threading.Event()
        self.stopEvent.clear()
        self.pushButton_3.clicked.connect(self.stopEvent.set)
        # self.pushButton_4.clicked.connect(self.caiji_calculate)


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
            name_dir = "E:/pycharm_project/backup2022_12_5/Qt-Camera/" + name
            # print(name_dir)
            global name2_dir
            name2_dir = "E:/pycharm_project/backup2022_12_5/Qt-Camera/" + name2
            # cv2.imwrite(img,name)
            # time.sleep(0.3)
            # shutil.copyfile("ZED1.jpg", name)

            # depth_cv_mix.inference(depth_pic_path=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\depth\depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
            # depth_cv_mix.inference(depth_pic_path="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/depth/depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
            # 拍车头
            depth_cv_elli_singlePic.inference_wood(depth_pic_path=name2_dir, input_dir=name_dir)

        except Exception as e:
            print(e)
    def capture(self):#拍车尾

        try:
            self.label_2.setPixmap(QPixmap("ZED1.png"))

            name = "pic/" + time.strftime("%Y%m%d%H%M%S") + ".png"
            name2 = "pic/depth" + time.strftime("%Y%m%d%H%M%S") + ".png"
            self.label_2.pixmap().save(name)
            print(name)
            # img = cv2.imread("ZED1.jpg")
            time.sleep(0.3)
            # img = cv2.imread("ZED1.jpg")
            shutil.copyfile("ZED2.png", name2)
            global name_dir
            name_dir = "E:/pycharm_project/backup2022_12_5/Qt-Camera/" + name
            # print(name_dir)
            global name2_dir
            name2_dir = "E:/pycharm_project/backup2022_12_5/Qt-Camera/" + name2
            # cv2.imwrite(img,name)
            # time.sleep(0.3)
            # shutil.copyfile("ZED1.jpg", name)

            # depth_cv_mix.inference(depth_pic_path=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\depth\depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir=r"\home\zsw\mmdetection-2.19.1\zed_pic\1.5\DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
            # depth_cv_mix.inference(depth_pic_path="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/depth/depth_PNG_22131528_1242_17-04-2022-16-20-24.png", input_dir="/home/zsw/mmdetection-2.19.1/zed_pic/1.5/DepthViewer_Left_22131528_1242_17-04-2022-16-20-10.png")
            # 拍车尾
            depth_cv_elli_singlePic.inference_wood(depth_pic_path=name2_dir, input_dir=name_dir)

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
            #cam = sl.Camera()
            init = sl.InitParameters()
            init.camera_resolution = sl.RESOLUTION.HD2K  # 将摄像头分辨率设为2K
            init.depth_maximum_distance = 5
            init.depth_minimum_distance = 0.5
            init.camera_fps = 15  # Set fps at 15帧数率为30fps
            init.depth_mode = sl.DEPTH_MODE.ULTRA

            self.cam = sl.Camera()

            if not self.cam.is_opened():
                print("Opening ZED Camera...")
            status = self.cam.open(init)
            if status != sl.ERROR_CODE.SUCCESS:
                print(repr(status))
                exit()

            runtime = sl.RuntimeParameters()
            runtime.sensing_mode = sl.SENSING_MODE.FILL  # Use FILL sensing mode 使用填充传感模式
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


                err = self.cam.grab(runtime)
                #cv2.namedWindow('ZED1', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
                # cv2.namedWindow('ZED2', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
                # cv2.namedWindow('ZED2', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
                if err == sl.ERROR_CODE.SUCCESS:
                    #左目图像
                    self.cam.retrieve_image(mat, sl.VIEW.LEFT)

                    #cv2.imwrite("ZED1.png", mat.get_data())

                    mat.write("ZED1.png")

                    # self.cam.retrieve_image(mat, sl.VIEW.DEPTH)
                    self.cam.retrieve_image(mat, sl.VIEW.DEPTH)
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
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(666, 488)
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
        self.tableWidget.setGeometry(QtCore.QRect(0, 60, 813, 371))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setStyleSheet("selection-background-color:pink")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.raise_()

        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(90, 20, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setIconSize(QtCore.QSize(18, 18))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("打开")
        MainWindow.setCentralWidget(self.centralWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.openfile)
        self.pushButton.clicked.connect(self.creat_table_show)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "测试"))


    def openfile(self):

        ###获取路径===================================================================

        openfile_name = QFileDialog.getOpenFileName(self,'选择文件','','Excel files(*.xlsx , *.xls)')
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

    ui.show()
    # apply_stylesheet(app, theme='dark_teal.xml')
    sys.exit(app.exec_())