import cv2
import numpy as np
import matplotlib.pyplot as plt


def find_particle_center(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 将图像转换为灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 对图像进行阈值处理
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 寻找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    # 循环处理每个轮廓
    for contour in contours:
        # 计算轮廓的中心坐标
        M = cv2.moments(contour)
        if M["m00"] != 0:
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])

            # 在图像上绘制中心点
            cv2.circle(image, (center_x, center_y), 5, (0, 255, 0), -1)

            # 在控制台输出中心坐标
            print("Particle Center Coordinates: ({}, {})".format(
                center_x, center_y))

    # 使用Matplotlib显示图像
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Image with Particle Center")
    plt.show()


# 使用示例
image_path = "cut2\frame_8340.jpg_cut.jpg"
find_particle_center(image_path)
