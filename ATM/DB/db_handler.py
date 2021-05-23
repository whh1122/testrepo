#！/usr/bin/env python3
# coding:utf-8
'''
数据处理层
    专门用来处理数据的
'''

import json,os
from conf import settings

# 查看数据
def select(username):
    # 1) 接收接口层传过来的username用户名，拼接用户json文件路径
    user_path = os.path.join(
        settings.USER_DATA_PATH,f'{username}.json'
    )
    # 2）校验用户json文件是否存在
    if os.path.exists(user_path):
        # 3）打开数据，并返回给接口层
        with open(user_path,mode='r',encoding='utf-8') as f:
            user_dic = json.load(f)
            return user_dic
    # 4) 不return，默认return None

# 保存数据(添加新数据或更新数据)
def save(user_dic):
    # 1)拼接用户的数据字典
    username = user_dic.get('username')

    # 根据用户的名字，拼接 用户名.json 文件路径
    user_path = os.path.join(
        settings.USER_DATA_PATH, f'{username}.json'
    )
    # 2) 保存用户数据
    with open(user_path, mode='w', encoding='utf-8') as f:
        json.dump(user_dic, f, ensure_ascii=False)  # ensure_ascii=False可以显示中文


























"""
@version:1.0
@author:wanghonghao
@file:db_handler.py
@time:2021/5/2 21:58
"""