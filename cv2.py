import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

rootPath = os.getcwd()
a = []
dirs = os.listdir(rootPath)
print(dirs)
for i in dirs:
    if os.path.splitext(i)[1] == ".JPG":
        a.append(i)
print(a)

equal_fraction = 1.0 / (len(a))
img2 = cv2.imread(str(a[0]))
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
output = np.zeros_like(img2)
for i in range(len(a)):
    img2 = cv2.imread(str(a[i]))
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    output = output + img2 * equal_fraction
cv2.imwrite('lena_gray.jpg', output)

