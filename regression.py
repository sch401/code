from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

# 幂函数拟合
x1data = [
    [4, 4, 10, 10, 10, 10, 10, 10, 40, 40],
    [0.4, 0.4, 0.2, 0.2, 0.4, 0.4, 0.6, 0.6, 0.4, 0.4],
    [0.5, 1, 0.5, 1, 0.5, 1, 0.5, 1, 0.5, 1],
]
ydata = [300, 340, 280, 300, 300, 340, 340, 380, 300, 320]
print(x1data[0])


def target_func(x1, a1, b1, b2, b3):
    return a1 * (x1[0] ** b1) * (x1[1] ** b2) * (x1[2] ** b3)


### 利用拟合函数求特征值 ###
popt, pcov = curve_fit(target_func, x1data, ydata)
# ### R^2计算 ###
calc_ydata = target_func(x1data, *popt)


# [target_func(i, popt[0], popt[1],popt[2], popt[3]) for i in x1data]
# print(calc_ydata)
res_ydata = np.array(ydata) - np.array(calc_ydata)
ss_res = np.sum(res_ydata**2)
ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

# 拟合的值
# y = [target_func(i, popt[0], popt[1]) for i in x1data]
plt.scatter(calc_ydata, ydata)
plt.xlabel("rot speed predicted")
plt.ylabel("rot speed real")
plt.legend()
plt.show()
### 输出结果 ###
print("a = %f  b = %f   R2 = %f" % (popt[0], popt[1], r_squared))

print(ydata, calc_ydata)
