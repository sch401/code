import pandas as pd
import numpy as np
import os

path = os.getcwd()
print(path)
name = []
a = 0
for root, dirs, files in os.walk(path):
    for file in files:
        if os.path.splitext(file)[1] == ".txt":
            a = a + 1
            t = os.path.splitext(file)[0]
            print(t)
            name.append(t)
print(name)
print(a)
totallist = pd.DataFrame()
for i in range(0, a):
    name[i] = name[i] + ".txt"
    sourcedata = pd.read_csv(name[i])
    sourcedata = sourcedata.iloc[18:, :]
    # print(sourcedata)
    new_col = ["Potential", "Current"]
    sourcedata.columns = new_col
    sourcedata = sourcedata.astype("float")
    thirdcolumn = sourcedata["Current"] * 1000 / 0.21465
    fourthcolumn = thirdcolumn * sourcedata["Potential"]
    sourcedata = pd.concat(
        [sourcedata, pd.DataFrame(thirdcolumn), pd.DataFrame(fourthcolumn)], axis=1
    )
    new_col = ["Potential", "Current", "C", "D"]
    sourcedata.columns = new_col
    # print(sourcedata)
    z1 = np.polyfit(sourcedata["Potential"], thirdcolumn, 3)
    p1 = np.poly1d(z1)
    a = p1.c[-1]

    z2 = np.polyfit(thirdcolumn, sourcedata["Potential"], 3)
    p2 = np.poly1d(z2)
    b = p2.c[-1]

    s1 = sourcedata["D"]
    s1_argmax = s1[s1 == s1.min()].index
    c = float(sourcedata["D"][s1_argmax])
    aa = float(sourcedata["Potential"][s1_argmax])
    cc = float(sourcedata["C"][s1_argmax])
    e = c / (a * b)
    list = [name[i], a, b, c, aa, cc, e]

    totallist = pd.concat([totallist, pd.DataFrame(list)], axis=1)
new_col = ["文件名", "系数1", "系数2", "ac乘积最小值", "ac乘积最小时a的值", "ac乘积最小时c的值", "然后e列除以cd乘积就行"]
totallist = totallist.T
totallist.columns = new_col
totallist.to_csv("111.csv", encoding="utf_8_sig")
