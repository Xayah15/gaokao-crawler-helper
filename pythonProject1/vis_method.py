# -*- coding: utf-8 -*-
import csv
import re
import matplotlib.pyplot as plt

# 更换字体，使其支持中文
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


# 获取纵坐标（专业对应的分数）
def get_score(filename):
    list = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            list.append(row[2])
        return list


# 获取纵坐标（专业对应的最低位次）
def get_section(filename):
    list = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            list.append(row[3])
        return list

# 获取横坐标（招生类型）
def get_zslx(filename):
    list = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            list.append(row[0])
        return list

# 获取横坐标（专业名称）
def get_name(filename):
    # 正则表达式提取第一个括号前的内容
    pattern = r'^(.*?)\）'
    list = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name = row[0]
            # 正则表达式 修改过长的专业名称 方便展示
            substring1 = "办学地点"
            substring2 = "包含专业"
            name = name.replace(substring1, '').replace(substring2, '')
            try:
                name = str(re.search(pattern, name).group(1))
                list.append(name)
            except AttributeError:
                list.append(name)

        return list

# 获取横坐标（年）
def get_year(filename):
    list = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            list.append(row[4])
        return list


# 启动折线统计图窗口（专业与最低分数线）
def showwindow(name, score):
    # 设置样式
    plt.style.use('fivethirtyeight')
    # 设置坐标系的数量（几幅图）,fig是图片,ax是图表
    fig, ax = plt.subplots(figsize=(16,9))
    # 设置横，纵坐标，可设置多个（传入参数的关键语句）
    plt.scatter(name, score, s=250, c='green', edgecolors='black', linewidth=1, alpha=0.7)
    # 倾斜横坐标
    fig.autofmt_xdate()
    # 翻转Y轴。使高分在上方，低分在下方
    plt.gca().invert_yaxis()
    # 设置标签
    ax.set(ylabel='最低分', title='各专业最低分数线')
    # 缩小横坐标尺寸
    plt.tick_params(axis='x', labelsize=8)
    # 全屏展示
    plt.tight_layout()
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()

    # 按钮
    def close(event):
        plt.close()
    ax_button = plt.axes([0.9, 0.9, 0.1, 0.07])
    button = plt.Button(ax_button, '关闭')
    button.on_clicked(close)

    plt.show()


