import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

rootPath = os.getcwd()
dirs = os.listdir(rootPath)
path = ['100','120', '140', '160', '180', '200', '220', '240','260','280','300','320','340','360','380','400','420','440']
# '100','120', '140', '160', '180', '200', '220', '240','260','280','300','320','340','360','380','400','420','440'
curve = pd.DataFrame()
filename = []
# rotation
def rotate(img, degree):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    scale = 1.0
    M = cv2.getRotationMatrix2D(center, degree, scale)
    img = cv2.warpAffine(img, M, (w, h))
    return img
# cutting
def cut(img,r1,r2,c1,c2):
    img = img[r1:r2, c1:c2]
    return img
# scaling
def scale(img):
    width = int(img.shape[1])
    height = int(img.shape[0])
    std = 1050
    scale_percent = std/width
    height = int(scale_percent*height)
    dim = (1050, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img
for sub in range(0, len(path)):
    dirs = os.listdir('.\\' + path[sub])
    for i in dirs:
        if os.path.splitext(i)[1] == ".JPG":
            filename.append(i)
    print(path[sub])
    equal_fraction = 1.0 / (len(filename))
    img = cv2.imread('.\\' + path[sub]+'\\'+str(filename[0]))
    img = rotate(img, 0.8)
    cv2.imwrite('.\\process\\' + path[sub]+'GRAY - rot.jpg', img)
    img = cut(img,1515,2971,1994,3154)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = scale(img)
    output = np.zeros_like(img)
    for i in range(len(filename)):
        img = cv2.imread('.\\' + path[sub]+'\\'+str(filename[i]))
        img = rotate(img, 0.8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cut(img,1515,2971,1994,3154)
        img = scale(img)
        output = output + 1/len(filename)*img
    cv2.imwrite('.\\process\\' + path[sub]+'GRAY - cut.jpg', output)
    filename = []
    img = cv2.imread('.\\process\\' +
                     path[sub]+'GRAY - cut.jpg', cv2.IMREAD_GRAYSCALE)
    clahe = cv2.createCLAHE(clipLimit=0.1, tileGridSize=(int(1/10*img.shape[1]), int(img.shape[0])))
    img = clahe.apply(img)
    cv2.imwrite('.\\process\\' + path[sub]+'GRAY - eq.jpg', img)
    img = cv2.GaussianBlur(img, (21,21),0)
    ret, thresh1 = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)
    cv2.imwrite('.\\process\\' + path[sub]+'GRAY - bi.jpg', thresh1)
    fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(16, 8),
                           constrained_layout=True)
    x = np.arange(0, thresh1.shape[0])
    ave = np.flipud(np.around(np.mean(thresh1, axis=1)))
    N = 35
    weights = np.ones(N) / N
    y_smooth = np.convolve(weights, ave, 'same')
    curve[sub] = y_smooth
    ax[0].plot(y_smooth, x)
    ax[0].set_ylim(0, thresh1.shape[0])
    ax[1].imshow(thresh1, cmap="gray")
    plt.title("Matplotlib demo")
    plt.xlabel("x axis")
    plt.ylabel("y axis")
    plt.savefig('.\\process\\' + path[sub]+'GRAY - compare.jpg')
curve.to_csv('.\\process\\curve.csv')
fig, ax = plt.subplots()
ax = curve.plot()
plt.savefig('.\\process\\' + path[sub]+'curve.jpg')

