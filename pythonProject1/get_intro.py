# -*- coding: utf-8 -*-
import csv

import requests

with open('DICT/school_ID.csv', encoding='gb2312') as f1:
    csvfile = csv.reader(f1)
    listf1 = list(csvfile)
    schoolID_dic = dict(listf1)

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "close"
}
index1 = '河南大学'
sch_id = schoolID_dic[f'{index1}']

resp = requests.get(url=f"https://static-data.gaokao.cn/www/2.0/school/{sch_id}/info.json", headers=header)
dic = resp.json()
plan_num = dic['data']['address']
print(resp.status_code)
print(plan_num)

