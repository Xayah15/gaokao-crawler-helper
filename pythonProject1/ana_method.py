# -*- coding: utf-8 -*-
import csv
import os
import re
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']    # 更换字体，使其支持中文
# 颜色字典：设置一个变量，给每一条折线使用不同的颜色，用于辨认
with open('DICT/color.csv', encoding='gb2312') as f1:
    csvfile = csv.reader(f1)
    listf1 = list(csvfile)
    color_dic = dict(listf1)

# 获取文件（指定学校的分组后文件）
def find_files(name):
    matching_files = []
    file = os.listdir('ana_show_csv')
    if name in file:
        for filename in os.listdir(f'ana_show_csv/{name}'):
            if name in filename:
                matching_files.append(os.path.join(f'ana_show_csv/{name}', filename))
            else:
                pass
        print(matching_files)
    else:
        print('分析未完成')
    return matching_files

# 获取年
def get_year(filename):
    list = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            list.append(int(row[4]))
        return list


# 获取最低分
def get_score(filename):
    list = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            list.append(int(row[2]))    # 转化成int类型，才能使不同的折线使用相同的坐标轴
        return list


# 获取名称列表
def group_csv(name):
    name_list = []
    pattern = re.compile(r'[\u4e00-\u9fff]+')    # 正则表达式（筛选中文文字，规范生成的csv文件名）
    df = pd.read_csv(f'ana_csv/{name}统计.csv', encoding='utf-8', header=0)
    groups = df.groupby(by=['招生类型'])    # 分组 将招生类型相同的放在一起
    for group_name, group_data in groups:
        type_name = pattern.findall(str(group_name))
        type_name = type_name[0]    # 分组得到的group_name(type_name)是一个列表，命名时需要转换成字符格式
        name_list.append(type_name)
    return name_list


# 获取招生类型
def get_zslx(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name = row[0]
            break
    return name


# 获取最低位次
def get_section(filename):
    list = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            list.append(int(row[3]))    # 转化成int类型，才能使不同的折线使用相同的坐标轴
        return list


# 数据分析窗口（位次）
def ana_window(matching_files, csv_name):

    plt.style.use('fivethirtyeight')    # 设置样式

    fig, ax = plt.subplots(figsize=(12, 6))    # 设置坐标系的数量（几幅图）,fig是图片,ax是图表
    num = 0
    try:
        for file in matching_files:
            year = get_year(file)
            section = get_section(file)
            name = get_zslx(file)
            # 设置横，纵坐标，可设置多个（传入参数的关键语句）
            plt.plot(year, section, label=name, marker='o', markersize=10, c=f"{color_dic[f'{num}']}",
                     linewidth=1, alpha=0.8, linestyle="-")
            # 显示每个点位的Y值（最低位次数字）
            for x, y in zip(year, section):
                plt.text(x, y, str(y), fontsize=9)
            num += 1

        plt.gca().invert_yaxis()    # 翻转Y轴。使高分在上方，低分在下方

        ax.set(ylabel='最低位次', title=f'{csv_name}近五年最低位次变化情况')    # 设置标签

        plt.tick_params(axis='x', labelsize=20)    # 横坐标尺寸
        plt.legend(fontsize=10, loc='upper left')    # 图例尺寸和位置
        plt.tight_layout()

        plt.show()
    except KeyError:
        pass


# 数据分析（分数）
def ana_window_score(matching_files, csv_name):
    plt.style.use('fivethirtyeight')    # 设置样式
    fig, ax = plt.subplots(figsize=(12, 6))    # 设置坐标系的数量（几幅图）,fig是图片,ax是图表
    num = 0
    try:
        for file in matching_files:
            year = get_year(file)
            score = get_score(file)
            name = get_zslx(file)
            # 设置横，纵坐标，可设置多个（传入参数的关键语句）
            plt.plot(year, score, label=name, marker='o', markersize=10, c=f"{color_dic[f'{num}']}",
                     linewidth=1, alpha=0.8, linestyle="-")
            # 显示每个点位的Y值（最低位次数字）
            for x, y in zip(year, score):
                plt.text(x, y, str(y), fontsize=9)
            num += 1

        ax.set(ylabel='最低分', title=f'{csv_name}近五年最低分变化情况')    # 设置标签

        plt.tick_params(axis='x', labelsize=20)    # 横坐标尺寸
        plt.legend(fontsize=10, loc='upper left')    # 图例尺寸和位置
        plt.tight_layout()

        plt.show()
    except KeyError:
        pass







