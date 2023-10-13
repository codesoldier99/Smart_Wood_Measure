from argparse import ArgumentParser
from mmdet.apis import inference_detector, init_detector, show_result_pyplot
# from calc_mea import measurement
# from icecream import ic
# halcon+aruco+depth
import os
import time
import numpy as np
import cv2
import math
import xlwt

# import halcon as ha
import os
import imutils

# from K_means_1d import K_means_1d
from Volume_Calculation import Volume_Calculation
# from detect_aruco import aruco_identify_by_picture
# from detect_aruco_4 import aruco_identify_by_picture
# from detect_aruco_2 import aruco_identify_by_picture
# from detect_aruco_un_P import aruco_identify_by_picture  # 一个ARUCO码

# from K_means_1d import K_means_1d
from statistics_diameter_and_volume_2_table import Statistics2Table
# from point_in_polygon import point_in_polygon
# from xlwt_get_max_col import get_max_col
from depth_test_PIL import getPngPix
from FillHole import FillHole

def inference_wood(depth_pic_path, input_dir):
    print(depth_pic_path)
    print(input_dir)
    fout = ""
    start_time = time.time()
    # markerLength = 0.3025
    K = 1  # 不分层
    # K = 2  # 分层，默认下层
    # 检尺长
    tree_longl = 4
    # 圆度
    # Circularity_threshold=0.6

    # 深度阈值 车尾约2500 车头约1600，单位mm
    Depth_threshold = 2500
    # 深度图像地址
    depth_pic_path = r"C:\backup2022_12_5\backup2022_12_5\Qt-Camera\pic\depth20220803122712.png"
    input_dir = r"C:\backup2022_12_5\backup2022_12_5\Qt-Camera\pic\20220803122712.png"

    #0
    # depth_pic_path = r"D:\wood\mmlab\volume\ph\ph11\depth_PNG_37317637_1242_14-03-2023-15-03-26.png"
    # input_dir = r"D:\wood\mmlab\volume\ph\ph11\DepthViewer_Left_37317637_1242_14-03-2023-15-03-22.png"
    #1
    # depth_pic_path = r"D:\wood\mmlab\volume\ph\ph11\depth_PNG_37317637_1242_14-03-2023-15-03-26.png"
    # input_dir = r"D:\wood\mmlab/volume\ph\ph11\DepthViewer_Left_37317637_1242_14-03-2023-15-03-22.png"
    # 2
    # input_dir = os.getcwd() + 'pic/20220803122712.png'
    # depth_pic_path = os.getcwd() + 'pic/depth20220803122712.png'
    # 3
    # depth_pic_path = r"D:\wood\mmlab\volume\ph2\7a4241ef7e993aa8386455cc9c4d914.png"
    # input_dir = r"D:\wood\mmlab\volume\ph2\d5686d36c8026b3634e519ff43a4adc.png"
    # 结果保存路径
    output_dir =r"c:\result"
    # 自动在输入路径下生成最终结果的文件夹
    # output_dir = input_dir + '/' + 'cv_result_mix_min'

    # 模型配置文件地址
    config_dir = r'C:\backup2022_12_5\backup2022_12_5\tree_test\xuezhang\mask_rcnn_r2_101_fpn_1x_coco_wood.py'
    checkpoint_dir = r'C:\backup2022_12_5\backup2022_12_5\tree_test\xuezhang\epoch_36.pth'
    # config_dir = r"D:\wood\mmlab\volume\weight\mask_rcnn_r2_101_fpn_1x_coco_wood.py"
    # checkpoint_dir = r"D:\wood\mmlab\volume\weight\epoch_36.pth"
    # config_dir = r"F:\data\coco_1\0.661-1000-v1_b_albu\mask_rcnn_swin-t-p4-w7_fpn_fp16_ms-crop-3x_coco.py"
    # checkpoint_dir = r"F:\data\coco_1\0.661-1000-v1_b_albu\epoch_36.pth"
    # config_dir = r"F:\data\coco_1\0.661-1000-v1_b\mask_rcnn_swin-t-p4-w7_fpn_fp16_ms-crop-3x_coco.py"
    # checkpoint_dir = r"F:\data\coco_1\0.661-1000-v1_b\epoch_36.pth"

    # config_dir = "F:\data\coco_1/0.661-1000-v1_b\mask_rcnn_swin-t-p4-w7_fpn_fp16_ms-crop-3x_coco.py"
    # checkpoint_dir ="F:\data\coco_1/0.661-1000-v1_b\epoch_36.pth"

    # config_dir ="F:\data\work_dirs\htc_r101_fpn_20e_coco\htc_r101_fpn_20e_coco.py"
    # checkpoint_dir ="F:\data\work_dirs\htc_r101_fpn_20e_coco\epoch_20.pth"


    # config_dir ="D:\wood\mmlab/volume\weight\mask_rcnn_r2_101_fpn_1x_coco_wood.py"
    # checkpoint_dir="D:\wood\mmlab/volume\weight\epoch_36.pth"

    # GPU or cpu
    #device = 'cuda:0'
    device = 'cpu'
    # 置信度
    score_thr = 0.6

    # 如果结果保存路径不存在，则创建文件夹
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    model = init_detector(config_dir, checkpoint_dir, device=device)

    ratio_list = list()
    ratio = 0.0008800518873684316
    ids = 0
    paths = input_dir

    # for j in range(0, len(count)):
    #
    #     paths = os.path.join(input_dir, count[j])
    #
    #     if os.path.isfile(paths) and (paths.endswith('bmp') or paths.endswith('png') or paths.endswith('jpg')):
    # print("testing: [{}/{}]".format(j + 1, len(count)))
    # start_time = time.time()

    # Area_SSSS = 0
    # Area_SSS = 0
    # Area_SS = 0
    # Area_S = 0
    # Area_M = 0
    # Area_L = 0
    # area_one_pic = 0
    # bbox_Area_SSSS = 0
    # bbox_Area_SSS = 0
    # bbox_Area_SS = 0
    # bbox_Area_S = 0
    # bbox_Area_M = 0
    # bbox_Area_L = 0
    volume_total = 0
    volume_total1 = 0

    file = os.path.basename(paths)  # 文件完整名
    filename = os.path.splitext(file)[0]  # 文件名
    filetype = os.path.splitext(file)[1]  # 文件扩展名
    #
    # filedir = os.path.join(outputdir, filename + '_' + 'out' + filetype)  # 用字符串函数zfill 以0补全所需位数
    # str(str(i).zfill(2))
    # img = paths
    # img_copy = img
    # rectify_pic_path, ratio, ids, distance, pitch, aruco_central_point = aruco_identify_by_picture(paths, markerLength=markerLength, central_point_flag=True)
    # rectify_pic_path, ratio, ids, distance, aruco_central_point = aruco_identify_by_picture(paths, markerLength=markerLength, central_point_flag=True)

    if ratio != 1:
        # print(ratio)
        ratio_list.append(ratio)
    img = paths
    # img = rectify_pic_path
    img_copy = img

    img = cv2.imread(img)
    height, width = img.shape[:2]
    color_mask = 255
    # img_black = np.zeros((height, width), dtype=np.float32)  # 生成黑色背景图做底图

    # test a single image
    result = inference_detector(model, img)

    if isinstance(result, tuple):
        bbox_result, segm_result = result

    bboxes = np.vstack(bbox_result)
    arrSortedIndex = np.lexsort((bboxes[:, 0], bboxes[:, 1]))  # numpy的多维数组排序，先排第1列，再排第0列，逆序排
    # aaa = len(arrSortedIndex)
    bboxes = bboxes[arrSortedIndex, :]

    if K == 2:  # 默认挑选出下层木材，否则检测全部木材  2 分层
        bboxes_lup_y_list = np.array(bboxes[:, 1]).reshape(-1, 1)  # 取 bboxes 左上角坐标的y轴数据
        bboxes_lup_x_list = np.array(bboxes[:, 0]).reshape(-1, 1)  # 取 bboxes 左上角坐标的y轴数据
        # bboxes_lup_xy_list = np.array(bboxes[:, :1])  # 取 bboxes 左上角坐标的xy轴数据
        bboxes_lup_xy_list = np.concatenate((bboxes_lup_x_list, bboxes_lup_y_list),
                                            axis=1)  # 拼接 bboxes 左上角坐标的x轴和y轴数据
        # bboxes_lup_xy_list = np.concatenate((bboxes_lup_y_list, bboxes_lup_x_list), axis=1)  # 拼接 bboxes 左上角坐标的x轴和y轴数据
        '''  调用cv2的K均值聚类算法
        '''
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        # 设置参数flags的值
        # flags = cv2.KMEANS_RANDOM_CENTERS
        flags = cv2.KMEANS_PP_CENTERS
        retval, bestLabels, centers = cv2.kmeans(bboxes_lup_xy_list, K, None, criteria, 50, flags)
        # bestLabels = np.sort(bestLabels, axis=0)  # 排序后莫名其妙有些木材丢失
        if bestLabels[0][0] == 0:  # 默认情况下，bestLabels中元素以0开始时，能成功绑定木材下层
            Indices = [n for n, x in enumerate(bestLabels) if x[0] == 1]  # 查找列表中重复元素的索引
        else:
            Indices = [n for n, x in enumerate(bestLabels) if x[0] == 0]  # 查找列表中重复元素的索引
        # if K == 2:  # 默认挑选出下层木材
        #     Indices = [n for n, x in enumerate(bestLabels) if x[0] == 0]  # 查找列表中重复元素的索引
        # else:
        #     Indices = [n for n, x in enumerate(bestLabels) if x[0] == 1]
        arrSortedIndex = arrSortedIndex[Indices]
        bboxes = bboxes[Indices, :]
    if segm_result is not None:  # non empty
        # segms = mmcv.concat_list(segm_result)
        segms = segm_result[0]
        inds = np.where(bboxes[:, -1] > score_thr)[0]
        # np.random.seed(42)
        # color_masks = [
        #     np.random.randint(0, 256, (1, 3), dtype=np.uint8)
        #     for _ in range(max(labels) + 1)
        # ]
        count1 = 1
        count_circle = 0
        jingjitongji_list = list()
        jingjitongji_list1 = list()
        distance_p2p_list = list()
        depth_list = list()

        # 三维黑色图片
        img_black_3 = np.zeros((height, width, 3), dtype=np.uint8)  # 生成黑色背景图做底图,cv2
        img_black_3_halcon = np.zeros((height, width, 3), dtype=np.uint8)  # 生成黑色背景图做底图, 3维

        for i in inds:
            i = int(i)
            img_black = np.zeros((height, width), dtype=np.uint8)  # 生成黑色背景图做底图
            # color_mask = color_masks[labels[i]]
            mask = segms[arrSortedIndex[i]].astype(bool)
            img_black[mask] = img_black[mask] * 0.5 + color_mask * 1
            img_black = FillHole(img_black)  # 空洞填充
            area = cv2.countNonZero(img_black)  # 所有非空像素面积，与halcon/labelme计算相同
            # area_one_pic = area_one_pic + area
            # 检测到遮罩中的轮廓   并提取最大的轮廓-该轮廓将代表图像中给定对象的轮廓/边界。
            cnts = cv2.findContours(img_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)
            # 计算圆度
            # Circularity = (cv2.contourArea(cnts[0]) * 4 * math.pi)/(math.pow(cv2.arcLength(cnts[0], True), 2))
            # print(Circularity)

            #
            # # 根据圆度进行不同拟合
            # if Circularity < Circularity_threshold:  # 将长扁椭圆的原始轮廓拟合成圆
            #     count_circle += 1
            #     ((x, y), r) = cv2.minEnclosingCircle(c)
            #     cv2.circle(img, (int(x), int(y)), int(r), (0, 255, 0), 2)
            #
            # else:
            #     # (x, y), (a, b), angle = cv2.fitEllipse(cnt)
            #     # ellipse =  [ (x, y) , (a, b), angle ]
            #     # ellipse
            #     # 为元组类型，其里面的参数为：
            #     # （x, y）代表椭圆中心点的位置
            #     # （a, b）代表长短轴长度，应注意a、b为长短轴的直径，而非半径
            #     # angle
            #     # 代表了中心旋转的角度
            #     ((x,y),(ra,rb),Phi)= cv2.fitEllipse(c)
            #     # print(ra)
            #     cv2.ellipse(img, ((x, y), (ra, rb), (180 - Phi * 180 / math.pi)),
            #                 (0, 255, 0), 2)
            #     theta = Phi * 180
            #     # 长径与短径的均值
            #     # rb = min(ra,rb)
            #     rb = (ra + rb) / 2.0
            #     # rb2 = max(ra, rb).
            #
            #
            # depth_XY_data = getPngPix(pngPath=depth_pic_path, pixelX=x, pixelY=y)
            # depth_list.append(depth_XY_data)
            # if Circularity < Circularity_threshold:
            #     (x1, y1) = (x - r, y)  # 圆左顶点
            #     (x2, y2) = (x + r, y)  # 圆右顶点
            # else:
            #     # (x1, y1) = (x + 0.5*rb * np.sin(theta), y + 0.5*rb * np.cos(theta))  # 椭圆上顶点
            #     # (x2, y2) = (x - 0.5*rb * np.sin(theta), y - 0.5*rb * np.cos(theta))  # 椭圆下顶点
            #
            #     (x1, y1) = (x + 0.5*rb, y)
            #     (x2, y2) = (x - 0.5*rb, y)  # 椭圆下顶点
            # D = depth_XY_data * np.sqrt((x1-x2)*(x1-x2)/(1050.23 * 1050.23) + (y1-y2)*(y1-y2)/(1050.23 * 1050.23))/10.0
            #
            # D1 = D
            #
            # ((x, y), (ra, rb), Phi) = cv2.fitEllipse(c)
            # # print(ra)
            # cv2.ellipse(img, ((x, y), (ra, rb), (180 - Phi * 180 / math.pi)),
            #             (0, 255, 0), 2)
            # theta = Phi * 180
            # # 长径与短径的均值
            # # rb2 = min(ra,rb)
            # rb2 = (ra + rb) / 2.0
            # # rb2 = max(ra, rb)
            #
            ((x, y), (ra, rb), Phi) = cv2.fitEllipse(c)
            # print(Phi)
            # 椭圆拟合
            cv2.ellipse(img, ((x, y), (ra, rb), Phi),
                        (0, 255, 0), 2)
            theta = Phi * 180

            #
            # ell min -9.47%,aver -4.01，max 1.26%
            # 检尺径取最小径
            # rb = min(ra, rb)
            # 检尺径取均值
            rb = (ra + rb) / 2.0
            # 检尺径取最大值
            # rb = max(ra, rb)
            # 读取深度值
            depth_XY_data = getPngPix(pngPath=depth_pic_path, pixelX=x, pixelY=y)
            # depth_XY_data = 1
            # print(depth_XY_data)
            # 计算深度阈值范围内的结果
            if depth_XY_data > 0 and depth_XY_data <= Depth_threshold:
                depth_list.append(depth_XY_data)
            # (x1, y1) = (x + 0.5*rb * np.sin(theta), y - 0.5*rb * np.cos(theta))  # 椭圆上顶点
            # (x2, y2) = (x - 0.5*rb * np.sin(theta), y + 0.5*rb * np.cos(theta))  # 椭圆下顶点
            (x1, y1) = (x + 0.5 * rb * np.sin(theta), y + 0.5 * rb * np.cos(theta))  # 椭圆上顶点
            (x2, y2) = (x - 0.5 * rb * np.sin(theta), y - 0.5 * rb * np.cos(theta))  # 椭圆下顶点

            # zed2i_2mm
            D = depth_XY_data * np.sqrt(
                (x1 - x2) * (x1 - x2) / (1049.29 * 1049.29) + (y1 - y2) * (y1 - y2) / (1049.29 * 1049.29)) / 10.0
            # aver1.03   最终结果取1.03的补偿系数
            # D = depth_XY_data * np.sqrt((x1 - x2) * (x1 - x2) / (1049.29 * 1049.29) + (y1 - y2) * (y1 - y2) / (1049.29 * 1049.29)) / (10.0*1.03)
            # zed2i_4mm
            # D = depth_XY_data * np.sqrt((x1 - x2) * (x1 - x2) / (1962.626 * 1962.626) + (y1 - y2) * (y1 - y2) / (1962.626 * 1962.626)) / 10.0
            # aver1.03
            # D = depth_XY_data * np.sqrt((x1 - x2) * (x1 - x2) / (1962.626 * 1962.626) + (y1 - y2) * (y1 - y2) / (1962.626 * 1962.626)) / (10.0*1.03)

            D1 = D

            #
            # 预测的小数木材尺径转换为整数偶数尺径
            if int(D) % 2 == 0:  # 偶数
                D = int(D)
            else:
                D = int(D) - 1
            if depth_XY_data > 0 and depth_XY_data <= Depth_threshold:
                volume = Volume_Calculation(tree_longl, D)
                volume_total = volume_total + volume
                # 预测的小数木材尺径转换为1位小数尺径
                D1 = round(D1, 1)
                volume1 = Volume_Calculation(tree_longl, D1)
                volume_total1 = volume_total1 + volume1

            # 打印预测尺径
            # cv2.putText(img, "{}".format(D1), (int(x) - 18, int(y) + 8),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)      # 200万像素图片
            # cv2.putText(img, "{}".format(D1), (int(x) - 23, int(y) + 14),
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)        # 800万像素图片
            # 打印序号和尺径
            # if depth_XY_data >0 and depth_XY_data <=Depth_threshold:
            # mobile
            # 预测图中，仅显示深度值在0~深度阈值内的结果，不在范围内的只显示轮廓
            if depth_XY_data > 0 and depth_XY_data <= Depth_threshold:
                cv2.putText(img, "{}".format(count1), (int(x) - 18, int(y) - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)  # 800万像素图片
                # 小数
                cv2.putText(img, "{}".format(D1), (int(x) - 18, int(y) + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)  # 800万像素图片
                # 偶数
                # cv2.putText(img, "{}".format(D), (int(x) - 18, int(y) + 30),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)          # 800万像素图片
                jingjitongji_list.append(D)
                # print(jingjitongji_list)
                jingjitongji_list1.append(D1)
                count1 += 1
            # print(count1)
            # win_name = 'mask'
            # cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
            # cv2.resizeWindow(win_name, 1200, 900)  # 限制显示窗口大小
            # cv2.imshow(win_name, img)
            # # cv2.imshow('mask', img_black)
            # cv2.waitKey(0)
        # 真实根数需要-1
        Number = count1 - 1
        # 统计数据整合(segm)
        # Area_SSSS_Tatal = Area_SSSS_Tatal + Area_SSSS
        # Area_SSS_Tatal = Area_SSS_Tatal + Area_SSS
        # Area_SS_Tatal = Area_SS_Tatal + Area_SS
        # Area_S_Tatal = Area_S_Tatal + Area_S
        # Area_M_Tatal = Area_M_Tatal + Area_M
        # Area_L_Tatal = Area_L_Tatal + Area_L
        # NUmber_Tatal = NUmber_Tatal + Number
        # area_all_pic = area_all_pic + area_one_pic
        #
        # # 统计数据整合(bbox)
        # bbox_Area_SSSS_Tatal = bbox_Area_SSSS_Tatal + bbox_Area_SSSS
        # bbox_Area_SSS_Tatal = bbox_Area_SSS_Tatal + bbox_Area_SSS
        # bbox_Area_SS_Tatal = bbox_Area_SS_Tatal + bbox_Area_SS
        # bbox_Area_S_Tatal = bbox_Area_S_Tatal + bbox_Area_S
        # bbox_Area_M_Tatal = bbox_Area_M_Tatal + bbox_Area_M
        # bbox_Area_L_Tatal = bbox_Area_L_Tatal + bbox_Area_L
        # NUmber_Tatal = NUmber_Tatal + Number

        # cv2.putText(img, "Number:{}={}+{}+{}".format(Number, Area_S, Area_M, Area_L), (0, 50),
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        # 统计数量、尺径和材积
        # cv2.putText(img, "Id:{},Number:{},Volume:{:.4f},Volume1:{:.4f}".format(ids, Number, volume_total, volume_total1), (0, 50),
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)        # 200万
        #
        # cv2.putText(img,
        #             "Id:{},Number:{},Volume:{:.4f},Volume1:{:.4f}".format(ids, Number, volume_total, volume_total1),
        #             (0, 100),
        #             cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 8)        # 800万
        #
        cv2.putText(img,
                    "Number:{},Volume:{:.4f},Volume1:{:.4f}".format(Number, volume_total, volume_total1),
                    (0, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 6)  # 800万
        #
        # 增加每像素边长 ratio 的显示
        # cv2.putText(img,
        #             "Ratio:{:.8f}".format(ratio), (0, 250), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 10)  # 800万

        # win_name = 'mask'
        # cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
        # w = int(width / 2)
        # h = int(height/2)
        # cv2.resizeWindow(win_name, (w, h))  # 限制显示窗口大小height, width
        # cv2.imshow(win_name, img)
        # cv2.imshow('mask', img_black)
        # cv2.waitKey(0)

        filedir_out = os.path.join(output_dir, filename + '_' + 'cv2_mea_p' + filetype)
        fout = filedir_out
        # filedir_out2 = os.path.join(output_dir2, filename + '_' + 'cv2_mea_p' + filetype)
        cv2.imwrite(filedir_out, img)

        # 将预测尺径信息保存进Excel
        xlsx_out_path = os.path.join(output_dir, filename + '_' + 'mea_volume_c' + '.xls')
        Statistics2Table(jingjitongji_list, jingjitongji_list1, depth_list, xlsx_out_path, tree_type='杉木',
                         tree_long=tree_longl)

    # show the results
    # show_result_pyplot(output_dir, model, img_copy, result, score_thr=score_thr, bboxes_show=False)
    # print('预测第{}张图片耗时：{}s'.format(j+1, time.time()-start_time))
    # file_out, file_mask = show_result_pyplot(output_dir, model, img, result, score_thr=score_thr, bboxes_show=False)
    # outfile, jingji = measurement(file_mask, img)

    # else:
    #     continue

    print("测试完毕！")
    # Real_Ratio_All = NUmber_Tatal / Real_Number_Tatal * 100
    # Real_Ratio_All1 = Real_Ratio_All
    #
    # Real_Ratio_All = round(Real_Ratio_All-0.0005, 3)

    # print('bbox/segm：')
    # print('SSSS：{}/{}'.format(bbox_Area_SSSS_Tatal, Area_SSSS_Tatal))
    # print('SSS：{}/{}'.format(bbox_Area_SSS_Tatal, Area_SSS_Tatal))
    # print('SS：{}/{}'.format(bbox_Area_SS_Tatal, Area_SS_Tatal))
    # print('S：{}/{}'.format(bbox_Area_S_Tatal, Area_S_Tatal))
    # print('M：{}/{}'.format(bbox_Area_M_Tatal, Area_M_Tatal))
    # print('L：{}/{}'.format(bbox_Area_L_Tatal, Area_L_Tatal))
    # print('检测/总数：{}/{}'.format(NUmber_Tatal, Real_Number_Tatal))
    # print('检测率：{:.3%}'.format(NUmber_Tatal/Real_Number_Tatal-0.000005))  # 截断保留百分号 3位
    # # print('检测率：{:.4%}'.format(NUmber_Tatal/Real_Number_Tatal))
    # print('数据集全部木材像素面积：{}'.format(area_all_pic))
    print('预测图片耗时：{}s'.format(time.time() - start_time))
    print('根数：{}'.format(Number))
    print('材积预测：{}m³'.format(volume_total))
    # ratio_mean = np.array(ratio_list).mean()
    # print('ratio_mean:{:.6f}'.format(ratio_mean))
    # print('圆拟合数量：{}'.format(count_circle))
    return fout
if __name__ == '__main__':
    # inference_wood("E:/depth_20230320143554.png",
    #           "E:/20230320143544.png")
    inference_wood("C:\backup2022_12_5\backup2022_12_5\Qt-Camera\pic\depth20220803122712.png",
    "C:\backup2022_12_5\backup2022_12_5\Qt-Camera\pic\20220803122712.png")

