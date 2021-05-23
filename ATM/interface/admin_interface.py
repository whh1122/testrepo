#！/usr/bin/env python3
# coding:utf-8

from DB import db_handler
from lib import common

admin_logger = common.get_logger(log_type='admin')

# 修改额度接口
def change_balance_interface(username,money):
    user_dic = db_handler.select(username)

    if username:
        # 修改额度
        user_dic['balance'] = int(money)
        # 保存修改后的用户数据
        db_handler.save(user_dic)

        msg = f'管理员修改用户{username}额度修改成功！'
        admin_logger.info(msg)
        return True, msg
    return False,f'{username}该用户不存在！'

# 冻结用户接口
def lock_user_interface(username):
    user_dic = db_handler.select(username)
    # 将locked默认值修改为True
    if user_dic:
        user_dic['locked'] = True
        db_handler.save(user_dic)
        msg = f'管理员冻结用户{username}成功！'
        admin_logger.info(msg)
        return True,msg
    return False,f'{username}不存在！'






"""
@version:1.0
@author:wanghonghao
@file:admin_interface.py
@time:2021/5/6 2:13
"""