import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

path = os.getcwd()
print(path)
name = []
a = 0
for root, dirs, files in os.walk(path):
    for file in files:
        if os.path.splitext(file)[1] == '.txt':
            a = a + 1
            t = os.path.splitext(file)[0]
            print(t)   
            name.append(t) 
print(name)
print(a)

# a = int(input("图中的曲线数目:"))
Area = float(input("面积:"))
# name = [None]*a

font1 = {'family' : 'Microsoft Yahei',
'weight' : 'normal',
'size'   : 15,
}

font2 = {'family' : 'Microsoft Yahei',
'weight' : 'normal',
'size'   : 10,
}


# for i in range(0,a):
#     I = i + 1
#     name[i] = input("第%d条曲线的文件名是："%(I))
#     name[i] = name[i] + '.txt'

for i in range(0,a):
    name[i] = name[i] + '.txt'
    df = pd.read_csv(name[i],delimiter=",")
    df = df.iloc[12:,:]
    # print(df)
    df = df.astype(float)
    # print(df)
    new_col = ['Potential', 'Current']
    df.columns = new_col
    thirdcolumn = df['Potential']+0.197+0.059*5
    # print(thirdcolumn)
    fourthcolumn = df['Current']*1000/Area
    # print(fourthcolumn)
    df['thirdcolumn'], df['fourthcolumn']= [thirdcolumn, fourthcolumn]
    print(df)
    plt.plot(thirdcolumn,fourthcolumn,label=name[i][:-4])
    legend = plt.legend(prop=font2,frameon=False)
plt.xlabel('Potential vs. RHE(V)',fontdict=font1)
plt.ylabel('Current density(mA cm$^{-2}$)',fontdict=font1)
plt.show() 


