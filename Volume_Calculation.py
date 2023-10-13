"""
_*_ coding utf-8 _*_
@File    : Volume_Calculation.py
@Time    : 2021/6/30 16:08
@Author  : YangPan
@Email   : younger6163@163.com
@Software: PyCharm
@Brief   : 木材材积计算公式
"""


def Volume_Calculation(L, D):  # 材积计算公式
    if L < 2:
        V = 0.8 * L * (D + 0.5 * L) ** 2 / 10000
    elif D < 14:
        V = 0.7854 * L * (D + 0.45 * L + 0.2) ** 2 / 10000
    else:
        V = 0.7854 * L * (D + 0.5 * L + 0.005 * L ** 2 + 0.000125 * L * (14 - L) ** 2 * (D - 10)) ** 2 / 10000
    # return '{:.3f}'.format(V)   # str返回
    if D < 8:
        return round(V, 4)
    else:
        return round(V, 3)  # 限定保留3位小数


if __name__ == '__main__':
    # D = [7.2, 7.0, 6.1, 3.8]
    D = [6, 6, 6, 4]
    for i, d in enumerate(D):
        volume = Volume_Calculation(2, d)
        print('d={},volume={}'.format(d, volume))
