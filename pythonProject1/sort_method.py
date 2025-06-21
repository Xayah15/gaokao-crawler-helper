# -*- coding: utf-8 -*-
import os
import re

import pandas as pd
# 添加表头
# data_csv = pd.read_csv(f'ana_csv/{name}统计.csv', header=None,
#                        names=['招生类型', '省控线', '最低分', '最低位次', '年'])
# data_csv.to_csv(f'ana_csv/{name}统计.csv')

# 同一招生类型近年最低位次的变化
def sort_class_min(name):
    df = pd.read_csv(f'ana_csv/{name}统计.csv', encoding='utf-8', header=0)

    df_result = df.sort_values(by=['招生类型', '最低位次'])
    df_result.to_csv(f'Final_ana_csv/{name}按招生类型统计.csv')
    print(df_result)


# 先按年份排序，再按当年的最低分
def sort_year_min(name):
    df = pd.read_csv(f'ana_csv/{name}统计.csv', encoding='utf-8', header=0)

    df_result = df.sort_values(by=['年', '最低位次'])
    df_result.to_csv(f'Final_ana_csv/{name}按年份统计.csv')
    print(df_result)


# 添加表头
def csv_header(self):
    name = str(self.lineEdit_sch.text())
    data_csv = pd.read_csv(f'ana_csv/{name}统计.csv', header=None,
                           names=['招生类型', '省控线', '最低分', '最低位次', '年'])
    data_csv.to_csv(f'ana_csv/{name}统计.csv')


# 分组（对无顺序的ana_csv）
def group_csv(name):
    folder_name = f"ana_show_csv/{name}"
    os.makedirs(folder_name)

    pattern = re.compile(r'[\u4e00-\u9fff]+')    # 正则表达式（筛选中文文字，规范生成的csv文件名）
    df = pd.read_csv(f'ana_csv/{name}.csv', encoding='utf-8', header=0)
    groups = df.groupby(by=['招生类型'])    # 分组 将招生类型相同的放在一起

    # 循环输出 将分组后的每个组都单独写入csv
    for group_name, group_data in groups:

        type_name = group_name[0]    # 分组得到的group_name(type_name)是一个列表，命名时需要转换成字符格式
        print(type_name)
        filename = f'{name}{type_name}.csv'
        group_data.to_csv(f'{folder_name}/{filename}', index=False)