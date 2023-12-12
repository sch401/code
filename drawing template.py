plt.rcParams["font.family"] = " Times New Roman, SimSun"
labelsize = 9
ticksize = 7
textsize = 12
ax.set_xlabel("实际甲烷产量 (mL/gVS)", fontsize=labelsize)
ax.set_ylabel("预测甲烷产量 (mL/gVS)", fontsize=labelsize)
ax.tick_params(labelsize=ticksize)
xmin, xmax, ymin, ymax = plt.axis()
ax.text(
    0.075 * (xmax - xmin) + xmin,
    0.85 * (ymax - ymin) + ymin,
    "C",
    fontsize=textsize,
)
fig.tight_layout()
