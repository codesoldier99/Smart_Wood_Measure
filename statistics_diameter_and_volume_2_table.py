"""
_*_ coding utf-8 _*_
@File    : statistics_diameter_and_volume_2_table.py
@Time    : 2021/7/9 11:50
@Author  : YangPan
@Email   : younger6163@163.com
@Software: PyCharm
@Brief   : 统计木材尺径和材积并保存进Excel
"""
import os
import xlwt
from Volume_Calculation import Volume_Calculation


def Statistics2Table(jingjitongji_list, jingjitongji_list1, distance_p2p_list, xlsx_out_path, tree_type, tree_long):
    # 将预测尺径信息保存进Excel
    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    # 创建sheet，Sheet1为表的名字，cell_overwrite_ok为是否覆盖单元格
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    # 设置单元格对齐方式
    style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
    al = xlwt.Alignment()
    al.horz = xlwt.Alignment.HORZ_CENTER  # 设置水平居中
    al.vert = xlwt.Alignment.VERT_CENTER  # 设置垂直居中
    style.alignment = al
    # 设置header
    header_0 = '序号'
    header_1 = '树材种'
    header_2 = '预测检尺径(小数)'
    header_3 = '预测检尺径(偶数)'
    # header_4 = '实际检尺长(小数)'
    # header_5 = '实际检尺长(偶数)'
    # header_6 = '误差(小数)'
    # header_7 = '误差(偶数)'
    header_4 = '深度信息'
    # 设置sheet1单元格宽度, 获取正确的字符个数
    sheet1.col(0).width = (len(header_0.encode('gb18030')) + 2) * 256  # 第0列宽度, '序号'列补充2字符间距
    sheet1.col(1).width = len(header_1.encode('gb18030')) * 256
    sheet1.col(2).width = len(header_2.encode('gb18030')) * 256
    sheet1.col(3).width = len(header_3.encode('gb18030')) * 256
    # sheet1.col(4).width = len(header_4.encode('gb18030')) * 256
    # sheet1.col(5).width = len(header_5.encode('gb18030')) * 256
    # sheet1.col(6).width = len(header_6.encode('gb18030')) * 256
    # sheet1.col(7).width = len(header_7.encode('gb18030')) * 256
    sheet1.col(4).width = len(header_4.encode('gb18030')) * 256

    # 向表中添加数据
    sheet1.write(0, 0, header_0, style=style)  # 第0行第0列
    sheet1.write(0, 1, header_1, style=style)  # 第0行第1列
    sheet1.write(0, 2, header_2, style=style)
    sheet1.write(0, 3, header_3, style=style)
    # sheet1.write(0, 4, header_4, style=style)
    # sheet1.write(0, 5, header_5, style=style)
    # sheet1.write(0, 6, header_6, style=style)
    # sheet1.write(0, 7, header_7, style=style)
    sheet1.write(0, 4, header_4, style=style)

    # jingjitongji_set = set(jingjitongji)
    # jingjitongji_set_list_sored = sorted(list(jingjitongji_set))
    # for i in range(len(jingjitongji_list)):  # 检尺径范围：4-60    29
    # for k, b, p in enumerate(zip(jingjitongji_list1, distance_p2p_list)):
    #     t_index = k + 1
    #     tree_type = tree_type
    #     t_long1 = b     # 检尺长
    #     distance_p2p = p  # 到Aruco码的距离
    #     # 预测的小数木材尺径转换为整数偶数尺径
    #     if int(b) % 2 == 0:  # 偶数
    #         t_long = int(b)
    #     else:
    #         t_long = int(b) - 1
    #     sheet1.write(k + 1, 0, t_index, style=style)  # 序号
    #     sheet1.write(k + 1, 1, tree_type, style=style)  # 树材种
    #     sheet1.write(k + 1, 2, t_long1, style=style)  # 检尺长(小数)
    #     sheet1.write(k + 1, 3, t_long, style=style)  # 检尺长(偶数)
    #     # 增加 到Aruco码的距离 信息
    #     sheet1.write(k + 1, 8, distance_p2p, style=style)  # 检尺长(偶数)

    for k in range(len(jingjitongji_list1)):
        t_index = k + 1
        tree_type = tree_type
        t_long1 = jingjitongji_list[k]  # 預測检尺径（小数）
        distance_p2p = distance_p2p_list[k]  # 到Aruco码的距离
        # 预测的小数木材尺径转换为整数偶数尺径
        if int(t_long1) % 2 == 0:  # 偶数
            t_long = int(t_long1)
        else:
            t_long = int(t_long1) - 1
        sheet1.write(k + 1, 0, t_index, style=style)  # 序号
        sheet1.write(k + 1, 1, tree_type, style=style)  # 树材种
        sheet1.write(k + 1, 2, t_long1, style=style)  # 检尺长(小数)
        sheet1.write(k + 1, 3, t_long, style=style)  # 检尺长(偶数)
        # 增加 到Aruco码的距离 信息
        sheet1.write(k + 1, 4, distance_p2p, style=style)  # 检尺长(偶数)

        # 统计偶数尺径木材的根数和材积
        # book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel

        # 创建sheet，Sheet1为表的名字，cell_overwrite_ok为是否覆盖单元格
    sheet2 = book.add_sheet(u'Sheet2', cell_overwrite_ok=True)
    # 设置header
    header1_0 = '树材种'
    header1_1 = '检尺长'
    header1_2 = '检尺径'
    header1_3 = '根数'
    header1_4 = '材积'
    # 设置sheet2单元格宽度, 获取正确的字符个数
    sheet2.col(0).width = len(header1_0.encode('gb18030')) * 256  # 第0列宽度
    sheet2.col(1).width = len(header1_1.encode('gb18030')) * 256
    sheet2.col(2).width = len(header1_2.encode('gb18030')) * 256
    sheet2.col(3).width = (len(header1_3.encode('gb18030')) + 2) * 256
    sheet2.col(4).width = (len(header1_4.encode('gb18030')) + 4) * 256  # '材积'列补充2字符间距
    # 向表中添加数据
    sheet2.write(0, 0, header1_0, style=style)  # 第0行第0列
    sheet2.write(0, 1, header1_1, style=style)  # 第0行第1列
    sheet2.write(0, 2, header1_2, style=style)
    sheet2.write(0, 3, header1_3, style=style)
    sheet2.write(0, 4, header1_4, style=style)

    jingjitongji_set = set(jingjitongji_list)
    jingjitongji_set_list_sored = sorted(list(jingjitongji_set))
    t_v_list = list()
    t_n_list = list()
    # for i in range(len(jingjitongji_list)):  # 检尺径范围：4-60    29
    for k, j in enumerate(jingjitongji_set_list_sored):
        tree_type = tree_type
        t_long = tree_long
        t_d = j
        t_n = jingjitongji_list.count(j)
        t_v = jingjitongji_list.count(j) * Volume_Calculation(t_long, j)
        t_v_list.append(t_v)
        t_n_list.append(t_n)
        sheet2.write(k + 1, 0, tree_type, style=style)  # 树材种
        sheet2.write(k + 1, 1, t_long, style=style)  # 检尺长
        sheet2.write(k + 1, 2, t_d, style=style)  # 检尺径
        sheet2.write(k + 1, 3, t_n, style=style)  # 根数
        sheet2.write(k + 1, 4, round(t_v, 4), style=style)  # 材积
    sheet2.write(len(jingjitongji_set_list_sored) + 1, 4, round(sum(t_v_list), 4), style=style)  # 总材积
    sheet2.write(len(jingjitongji_set_list_sored) + 1, 3, sum(t_n_list), style=style)  # 总根数
    # xlsx_out_path = os.path.join(output_dir, filename + '_' + 'mea_volume_c' + '.xlsx')
    book.save(xlsx_out_path)
