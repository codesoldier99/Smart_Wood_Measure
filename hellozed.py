import pyzed.sl as sl
import cv2
def hello_zed():
    # 创建相机对象
    zed = sl.Camera()  # Camera是非常重要的一个类

    # 创建初始化参数对象并配置初始化参数
    init_params = sl.InitParameters()
    init_params.sdk_verbose = False  # 相机有很多可以初始化的参数，用到一个认识一个
    init_params.camera_resolution = sl.RESOLUTION.HD2K
    # 打开相机（终端打开，但是看不到相机的画面，需要用到cv2.imshow显示相机画面，后面再介绍）
    err = zed.open(init_params)  # 指定参数打开相机
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)
    # 获得相机的信息，笔者列举了一部分，并不是全部信息，读者可以自行探究
    zed_info = zed.get_camera_information()
    print('相机序列号：%s' % zed_info.serial_number)
    print('相机型号：%s' % zed_info.camera_model)
    print('相机分辨率: width:%s, height:%s' % (zed_info.camera_resolution.width, zed_info.camera_resolution.height))
    print('相机FPS：%s' % zed_info.camera_fps)
    print('相机外部参数：')
    print('相机旋转矩阵R：%s' % zed_info.calibration_parameters.R)
    print('相机变换矩阵T：%s' % zed_info.calibration_parameters.T)
    print('相机基距：%s' % zed_info.calibration_parameters.get_camera_baseline())
    print('初始化参数：')
    zed_init = zed.get_init_parameters()
    print('相机分辨率：%s' % (zed_init.camera_resolution))
    print('深度最小：%s' % (zed_init.depth_minimum_distance))
    print('深度最大：%s' % (zed_init.depth_maximum_distance))
    # 关闭相机
    zed.close()

if __name__ == "__main__":
    hello_zed()
