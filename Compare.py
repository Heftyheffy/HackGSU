import cv2
import numpy as np

def getCompare(cnt2, num):
    img = cv2.imread('file.png', 0)
    if(num == 0):
    	img = cv2.imread('file2.png',0)
    #img2 = cv2.imread('file.png', 0)
    ret,thresh = cv2.threshold(img,127,255,0)
    cnt1,hierarchy = cv2.findContours(thresh, 1, 2)

    #ret,thresh = cv2.threshold(img2,127,255,0)
    #cnt2,hierarchy = cv2.findContours(thresh, 1, 2)

    ret = cv2.matchShapes(cnt1[0], cnt2,1, 0.0)
    return ret