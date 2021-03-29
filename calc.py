import time

import cv2
import numpy as np
from PIL import Image
from PyQt5 import QtWidgets, uic


def calculate(before_img_path, after_img_path, method='lucas_kanade'):
    if (method == 'lucas_kanade'):
        calculate_lucas_kanade(before_img_path, after_img_path)
    elif (method == 'farneback'):
        calculate_farneback(before_img_path, after_img_path)
    elif (method == 'farneback2'):
        calculate_farneback2(before_img_path, after_img_path)
    else:
        print('No such method found: ' + method)


def calculate_lucas_kanade(before_img_path, after_img_path):
    frame1 = cv2.imread(before_img_path)
    frame2 = cv2.imread(after_img_path)

    prvsImg = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    nextImg = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    feature_params = dict(maxCorners=100,
                          qualityLevel=0.3,
                          minDistance=7,
                          blockSize=7)
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    prevPts = cv2.goodFeaturesToTrack(prvsImg, mask=None, **feature_params)
    nextPts, status, err = cv2.calcOpticalFlowPyrLK(prvsImg, nextImg, prevPts, None, **lk_params)
    print(prevPts)
    print('------------')
    print(nextPts)


def calculate_farneback2(before_img_path, after_img_path):
    frame1 = cv2.imread(before_img_path)
    prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255

    frame2 = cv2.imread(after_img_path)
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    print(mag)
    print('-----------')
    print(ang)

    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow('frame2', rgb)


def calculate_farneback(before_img_path, after_img_path):
    frame1 = cv2.imread(before_img_path)
    frame2 = cv2.imread(after_img_path)

    prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs, next, 0., 0.5, 3, 15, 3, 5, 1., 0)

    horiz_arr = get_axis_value(flow, 0)
    #to_csv(horiz_arr, 'test/horiz.csv')
    vert_arr = get_axis_value(flow, 1)
    #to_csv(vert_arr, 'test/vert.csv')

    horz = cv2.normalize(flow[..., 0], None, 0, 255, cv2.NORM_MINMAX)
    vert = cv2.normalize(flow[..., 1], None, 0, 255, cv2.NORM_MINMAX)
    horz = horz.astype('uint8')
    vert = vert.astype('uint8')

    #save_text_to_file(flow)
    draw_image(horz)
    cv2.imshow('Horizontal Component', horz)
    cv2.imshow('Vertical Component', vert)


def draw_image(data):
    #data = data * 100
    img = Image.new('RGB', data.shape)
    img.putdata(data)
    img.show()

def save_text_to_file(num_values):
    filename = "test/output" + str(round(time.time() * 1000)) + ".txt"
    text_file = open(filename, "a")
    lst = num_values.tolist()
    for l in lst:
        text_file.write(str(l))
        text_file.write("\n")
    text_file.close()


def show_num_win(num_values):
    win = NumApp()
    win.setFixedSize(win.size())
    win.textBrowser.setText(str(num_values))
    win.show()

def get_axis_value(flow, axis=0):
    res = []
    for line in flow:
        line_arr = []
        for bivalue in line:
            line_arr.append(bivalue[axis])
        res.append(line_arr)
    return res

def to_csv(biarr, filename):
    with open(filename, 'a') as file:
        for line in biarr:
            for value in line:
                file.write(str(value))
                file.write(';')
            file.write('\n')



class NumApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('resources/numeric.ui', self)
