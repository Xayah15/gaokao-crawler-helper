# -*- coding: utf-8 -*-
import json


# 方法 将位次转化成23年对应分数
def sec_to_score(section):
    with open('Document/LK_score_section.json', 'r', encoding='gb2312') as file:
        # 使用json.load()方法解析JSON数据
        data = json.load(file)
    for key, value in data["data"]["search"].items():
        # print(f"Key: {key}")
        # print("rank_range:")
        # print(value['rank_range'])
        # print()
        start, end = map(int, value['rank_range'].split('-'))
        # 检查给定数字是否在范围内
        if start <= section <= end:
            print(key)
            return key
        else:
            pass

sec_to_score(450)
