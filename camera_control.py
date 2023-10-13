########################################################################
#
# Copyright (c) 2021, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################
# 待完善功能
# 展示两个画面，一个左目图像，一个深度图像，
# 图像名称修改
"""
    Live camera sample showing the camera information and video in real time and allows to control the different
    settings.
"""

import cv2
import pyzed.sl as sl
import time
camera_settings = sl.VIDEO_SETTINGS.BRIGHTNESS
str_camera_settings = "BRIGHTNESS"
step_camera_settings = 1


def main():
    print("Running...")
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD2K
    init.camera_fps = 15  # Set fps at 15
    init.depth_maximum_distance=2
    init.depth_minimum_distance=0.4
    # init.depth_mode = "ULTRA"
    cam = sl.Camera()
    if not cam.is_opened():
        print("Opening ZED Camera...")
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    runtime = sl.RuntimeParameters()
    runtime.sensing_mode = sl.SENSING_MODE.FILL  # Use FILL sensing mode
    # Setting the depth confidence parameters
    runtime.confidence_threshold = 100
    runtime.textureness_confidence_threshold = 100
    mat = sl.Mat()
    print_camera_information(cam)
    #print_help()

    key = ''
    while key != 113:  # for 'q' key
        err = cam.grab(runtime)
        cv2.namedWindow('ZED2', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        if err == sl.ERROR_CODE.SUCCESS:
            #左目图像
            # cam.retrieve_image(mat, sl.VIEW.LEFT)
            # cv2.imshow("ZED2", mat.get_data())
            # 深度图像
            cam.retrieve_image(mat, sl.VIEW.DEPTH)
            cv2.imshow("ZED2", mat.get_data())
            key = cv2.waitKey(5)
            settings(key, cam, runtime, mat)
        else:
            key = cv2.waitKey(5)
    cv2.destroyAllWindows()

    cam.close()
    print("\nFINISH")


def print_camera_information(cam):
    print("Resolution: {0}, {1}.".format(round(cam.get_camera_information().camera_resolution.width, 2), cam.get_camera_information().camera_resolution.height))
    print("Camera FPS: {0}.".format(cam.get_camera_information().camera_fps))
    print("Firmware: {0}.".format(cam.get_camera_information().camera_firmware_version))
    print("Serial number: {0}.\n".format(cam.get_camera_information().serial_number))


def print_help():
    print("Help for camera setting controls")
    print("  Increase camera settings value:     +")
    print("  Decrease camera settings value:     -")
    print("  Switch camera settings:             s")
    print("  Capture an image:                   c")
    print("  get a depth_image:                  d")
    print("  Reset all parameters:               r")
    print("  Record a video:                     z")
    print("  Quit:                             q\n")


def settings(key, cam, runtime, mat):
    if key == 115:  # for 's' key
        switch_camera_settings()
    elif key == 43:  # for '+' key
        current_value = cam.get_camera_settings(camera_settings)
        cam.set_camera_settings(camera_settings, current_value + step_camera_settings)
        print(str_camera_settings + ": " + str(current_value + step_camera_settings))
    elif key == 45:  # for '-' key
        current_value = cam.get_camera_settings(camera_settings)
        if current_value >= 1:
            cam.set_camera_settings(camera_settings, current_value - step_camera_settings)
            print(str_camera_settings + ": " + str(current_value - step_camera_settings))
    elif key == 99:  # for 'c' key
        capture(cam, runtime, mat)
    elif key == 100:  # for 'd' key
        depth(cam, runtime, mat)
    elif key == 114:  # for 'r' key
        cam.set_camera_settings(sl.VIDEO_SETTINGS.BRIGHTNESS, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.CONTRAST, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.HUE, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.SATURATION, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.SHARPNESS, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.GAIN, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE, -1)
        print("Camera settings: reset")
    elif key == 122:  # for 'z' key
        record(cam, runtime, mat)


def switch_camera_settings():
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


def record(cam, runtime, mat):
    vid = sl.ERROR_CODE.FAILURE
    out = False
    while vid != sl.ERROR_CODE.SUCCESS and not out:
        filepath = input("Enter filepath name: ")
        record_param = sl.RecordingParameters(filepath)
        vid = cam.enable_recording(record_param)
        print(repr(vid))
        if vid == sl.ERROR_CODE.SUCCESS:
            print("Recording started...")
            out = True
            print("Hit spacebar to stop recording: ")
            key = False
            while key != 32:  # for spacebar
                err = cam.grab(runtime)
                if err == sl.ERROR_CODE.SUCCESS:
                    cam.retrieve_image(mat)
                    cv2.imshow("ZED", mat.get_data())
                    key = cv2.waitKey(5)
        else:
            print("Help: you must enter the filepath + filename + SVO extension.")
            print("Recording not started.")
    cam.disable_recording()
    print("Recording finished.")
    cv2.destroyAllWindows()
# 抓取一张图片
def capture(cam, runtime, mat):
    # if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS:
        # A new image is available if grab() returns SUCCESS
        cam.retrieve_image(mat, sl.VIEW.LEFT)
        # # cam.retrieve_measure(mat, sl.MEASURE.DEPTH)
        #
        # # cv2.imshow("ZED", image.get_data())
        timestamp = cam.get_timestamp(sl.TIME_REFERENCE.CURRENT)  # Get the timestamp at the time the image was captured
        print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(mat.get_width(), mat.get_height(),
                                                                             timestamp.get_milliseconds()))

        img_name =  "/home/zsw/zed_pic/" + time.strftime("%Y%m%d%H%M%S") + ".png"
       # depth_name = 'G:/zed_pic/2022-3-4/1_depth.png'.format(time.time())
        mat.write(img_name)
        # dep = mat.write(depth_name)

# 获取深度图像
def depth(cam, runtime, mat):
    # if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS:
        # A new image is available if grab() returns SUCCESS
        # cam.retrieve_image(mat, sl.VIEW.LEFT)
        cam.retrieve_measure(mat, sl.MEASURE.DEPTH)

        # cv2.imshow("ZED", image.get_data())
        timestamp = cam.get_timestamp(sl.TIME_REFERENCE.CURRENT)  # Get the timestamp at the time the image was captured
        print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(mat.get_width(), mat.get_height(),
                                                                           timestamp.get_milliseconds()))
    # img_name = 'G:/zed_pic/2022-3-4/1.png'.format(time.time())
        depth_name = "/home/zsw/zed_pic/" +'depth'+ time.strftime("%Y%m%d%H%M%S") + ".png"
        # depth_name = "/home/zsw/zed_pic/1.png"

# img = mat.write(img_name)
        mat.write(depth_name)

if __name__ == "__main__":
    main()
