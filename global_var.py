# -*- coding: utf-8 -*-
import os

# 获取当前工作目录
path = os.path.dirname(os.path.abspath(__file__))
print(path)

 #拍照后保存路径
pic_path = path + '\\pic\\'
output_dir = path + '\\result\\'
print(pic_path)
# pic_filename = 'C:\\backup2022_12_5\\backup2022_12_5\\Qt-Camera\\pic\\20220803122712.png'  # 左图
# depth_pic_filename = 'C:\\backup2022_12_5\\backup2022_12_5\\Qt-Camera\\pic\\depth20220803122712.png'  #深度图
depth_threshold = 2500
model_configfile = r'C:\backup2022_12_5\backup2022_12_5\tree_test\xuezhang\mask_rcnn_r2_101_fpn_1x_coco_wood.py'
checkpoint_file = r'C:\backup2022_12_5\backup2022_12_5\tree_test\xuezhang\epoch_36.pth'
tree_longl = 4
# 深度阈值 车尾约2500 车头约1600，单位mm
Depth_threshold = 2500
# 深度计算设备  cpu or cuda：0

device = 'cpu'
def _init():  # 初始化
    global _global_dict
    _global_dict = {}








def set_value(key, value):
    # 定义一个全局变量
    _global_dict[key] = value


def get_value(key):
    # 获得一个全局变量，不存在则提示读取对应变量失败
    try:
        return _global_dict[key]
    except:
        print('读取' + key + '失败\r\n')
