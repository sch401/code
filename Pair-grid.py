import numpy as np
from scipy import stats
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "stix"
df = pd.read_excel("全时间拆分-拆-revised合并.xlsx", sheet_name="Sheet1")
plt.rcParams["axes.labelsize"] = 50
plt.rcParams['ytick.labelsize'] = 30
plt.rcParams['xtick.labelsize'] = 30


cmap = plt.get_cmap('coolwarm')



def column(y,**kws):
    sns.histplot(y,bins=5)
def corrfunc(x, y, **kws):
    r, _ = stats.pearsonr(x, y)
    color = cmap((r+1)/2)
    X = [x.min(),x.max()]
    plt.fill_between(X,y.min(),y.max(),color=color)
    plt.xlim(x.min(),x.max())
    plt.ylim(y.min(),y.max())
    plt.axis('off')
    plt.annotate("{:.2f}".format(r), xy=(.5, .5), ha='center', va='center',xycoords='axes fraction', fontsize=40)
    plt.tight_layout()

g = sns.PairGrid(df)
g.map_lower(plt.scatter)
g.map_diag(column)
g.map_upper(corrfunc)
plt.savefig("try.jpg",dpi=300)
