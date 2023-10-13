# from PIL import Image
# import numpy as np
# image =Image.open('444_1080.png')
# print(image)
# print(image.size)
# images = np.asarray(image)#转化成数组以后，iamges中存储的是图片的像素值。
# print(images[1,1])


from PIL import Image


def getPngPix(pngPath="2k_20depth_fill.png", pixelX=980, pixelY=727):
    img_src = Image.open(pngPath)
    # img_src = img_src.convert('RGBA')
    str_strlist = img_src.load()
    data = str_strlist[pixelX, pixelY]
    img_src.close()
    return data

#print(getPngPix())
