from cv2 import cv2
import matplotlib.pyplot as plt
import numpy as np
import math


def stackImages(scale, imgArray):
    '''
    图像堆栈，可缩放，按列表排列，不受颜色通道限制
    '''
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


# 简单方法画出漂亮的圆柱体（半径和高度均为1）

def Cylinder(r=1.0, h=1.0, color='Blues'):

    """
    Return a three-dimensional hollow cylinder that meets the conditions

    Parameters
    dtype: r= float : Radius, default value: 1.0
           h = float : Height, default value: 1.0
           color = str : Cylinder color, default value:Blues

    Returns
    -------
    3D picture

    See Also
    --------
    color=['Blues', 'BrBG', 'BuGn', 'BuPu', 'CMRmap', 'GnBu', 'Greens', 'Greys', 'OrRd', 'Oranges', 'PRGn',
           'PiYG', 'PuBu','PuBuGn', 'PuOr', 'PuRd', 'Purples', 'RdBu', 'RdGy', 'RdPu', 'RdYlBu', 'RdYlGn',
           'Reds', 'Spectral', 'Wistia','YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd', 'afmhot', 'autumn', 'binary',
           'bone', 'brg', 'bwr', 'cividis', 'cool', 'coolwarm', 'copper', 'cubehelix', 'flag', 'gist_earth',
           'gist_gray', 'gist_heat', 'gist_ncar', 'gist_rainbow', 'gist_stern', 'gist_yarg', 'gnuplot',
           'gnuplot2', 'gray', 'hot', 'hsv', 'inferno', 'jet', 'magma', 'nipy_spectral', 'ocean', 'pink',
           'plasma', 'rainbow', 'seismic', 'spring', 'summer', 'tab10', 'tab20b','tab20c', 'terrain', 'turbo',
           'twilight', 'twilight_shifted', 'viridis', 'winter'] or + '_r'
    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 生成圆柱数据，底面半径为r，高度为h。
    # 先根据极坐标方式生成数据
    u = np.linspace(0, 2 * np.pi, 50)  # 把圆分按角度为50等分
    h = np.linspace(0, h, 50)  # 把高度1均分为100份
    x = np.outer(r * np.sin(u), np.ones(len(h)))  # x值重复20次
    y = np.outer(r * np.cos(u), np.ones(len(h)))  # y值重复20次
    z = np.outer(np.ones(len(u)), h)  # x，y 对应的高度
    ax.plot_surface(x, y, z, cmap=plt.get_cmap(color))
    plt.show()


## Part of the function of the robot

def Degree_conversion(lis):
    lis1 = []
    for i in range(len(lis)):
        lis1.append(lis[i] / 180 * np.pi)
    return lis1