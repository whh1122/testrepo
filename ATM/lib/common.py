#！/usr/bin/env python3
# coding:utf-8
'''
存放公共方法
'''

import hashlib
from conf import settings
import logging.config

# md5加密
def get_pwd_md5(password):
    md5_obj = hashlib.md5()
    md5_obj.update(password.encode('utf-8'))
    salt = 'Iamsaltaddme'
    md5_obj.update(salt.encode('utf-8'))

    return md5_obj.hexdigest()

# 登录认证装饰器
def login_auth(func):
    from core import src
    def inner(*args,**kwargs):
        if src.login_user:
            res = func(*args,**kwargs)
            return res
        else:
            print('用户未登录，请登录！')
            src.login()
    return inner

# 添加日志功能(日志功能在接口层使用)
'''
https://www.bilibili.com/video/BV1QE41147hU?p=352&spm_id_from=pageDriver
'''
def get_logger(log_type):
    '''
    获取日志对象
    :param log_type: 比如是user日志，bank日志，商城日志
    :return:日志对象
    '''
    # 1）加载日志配置信息
    logging.config.dictConfig(
        settings.LOGGING_DIC
    )
    # 2）获取日志对象
    logger = logging.getLogger()
    return logger









"""
@version:1.0
@author:wanghonghao
@file:common.py
@time:2021/5/2 21:51
"""