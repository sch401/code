import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

rootPath = os.getcwd()
filename = []
dirs = os.listdir(rootPath)
for i in dirs:
    if os.path.splitext(i)[1] == ".JPG":
        filename.append(i)
print(filename)
equal_fraction = 1.0 / (len(filename))
img = cv2.imread(str(filename[0]))
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
output = np.zeros_like(img)
for i in range(len(filename)):
    img = cv2.imread(str(filename[i]))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output = output + img * equal_fraction
cv2.imwrite('GRAY.jpg', output)
img = cv2.imread('GRAY - cut.jpg', cv2.IMREAD_GRAYSCALE)
clahe = cv2.createCLAHE(clipLimit=17.5, tileGridSize=(75, 75))
img = clahe.apply(img)
plt.imshow(img, cmap='gray')
blur = cv2.GaussianBlur(img, (5, 5), 0)  
ret, thresh1 = cv2.threshold(blur, 125, 255, cv2.THRESH_BINARY)
cv2.imshow('BINARY', thresh1)
fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(8, 4),
                       constrained_layout=True)
x = np.arange(0, thresh1.shape[0])
ave = np.flipud(np.around(np.mean(thresh1, axis=1)))
N=25
weights = np.ones(N) / N
y_smooth = np.convolve(weights, ave, 'same')
ax[0].plot(y_smooth, x)
ax[0].set_ylim(0,thresh1.shape[0])
ax[1].imshow(thresh1, cmap="gray")
plt.title("Matplotlib demo")
plt.xlabel("x axis")
plt.ylabel("y axis")
plt.show()
