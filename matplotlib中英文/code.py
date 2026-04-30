font_path = r"E:\02生活\软件\RomanSong\RomanSong.ttf"
try:
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()
    print(f" 成功加载字体: {prop.get_name()}")
except Exception as e:
    print(f" 字体加载失败，请检查路径。错误信息: {e}")


warnings.filterwarnings('ignore')

plt.rcParams["mathtext.fontset"] = "stix"
