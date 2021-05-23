#！/usr/bin/env python3
# coding:utf-8
'''
程序的入口
'''

import os,sys

# 添加解释器环境变量
sys.path.append(os.path.dirname(__file__))

# 导入 第一层：用户视图层模块
from core import src

# 开始执行项目函数
if __name__ == '__main__':
    src.run()  # 1.先执行用户视图层



























"""
@version:1.0
@author:wanghonghao
@file:start.py
@time:2021/5/2 22:00
"""