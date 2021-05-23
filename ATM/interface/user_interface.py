#！/usr/bin/env python3
# coding:utf-8
'''
逻辑接口层
    用户接口
'''

from DB import db_handler
from lib import common

user_logger = common.get_logger(log_type='user')

# 注册接口
def register_interface(username,password,balace = 15000):
    # 2） 查看用户是否存在
    # 2.1） 调用数据处理层中的select函数，会返回用户字典或None
    user_dic = db_handler.select(username)

    # {user:user,pwd:pwd...} or None
    # 若用户存在，则return，告诉用户重新输入
    if user_dic:
        # return (False,'用户名已存在！')
        return False,'用户名已存在！'

    # 3） 若用户不存在，则保存用户数据
    # 做密码加密
    password = common.get_pwd_md5(password)

    # 3.1） 组织用户的数据字典信息
    user_dic = {
        'username': username,
        'password': password,
        'balance': balace,
        # 用于记录用户流水的列表
        'flow': [],
        # 用于记录用户购物车
        'shop_car': {},
        # locked：用于记录用户是否被冻结，False：未冻结，Ture：已被冻结
        'locked': False

    }
    # 3.2) 保存数据
    db_handler.save(user_dic)
    msg = f'{username}注册成功！'
    # 3.3) 记录日志
    user_logger.info(msg)
    return True,msg

# 登录接口
def login_interface(username,password):

    # 1）先查看当前用户数据是否存在
    # {return user_dic} or None
    user_dic = db_handler.select(username)
    # 用于判断用户是否存在
    # 若有冻结用户，则需要判断是否被锁定

    # 2）判断用户是否存在
    if user_dic:
        if user_dic.get('locked'):
            return False, f'用户{username}当前已被锁定！'

        # 给用户输入的密码做一次加密
        password = common.get_pwd_md5(password)
        # 3）校验密码是否一致
        if password == user_dic.get('password'):
            msg = f'用户：{username}登录成功！'
            user_logger.info(msg)
            return True,msg
        else:
            msg = '密码错误！'
            user_logger.warn(msg)
            return False,msg

    msg = '用户不存在，请重新输入！'
    # user_logger.warn(msg)
    return False,msg

# 查看余额接口
def check_bal_interface(username):
    user_dic = db_handler.select(username)
    return user_dic['balance']

# 查看购物车接口
def check_car_interface(username):
    user_dic = db_handler.select(username)
    return user_dic['shop_car']
"""
@version:1.0
@author:wanghonghao
@file:user_interface.py
@time:2021/5/2 21:54
"""