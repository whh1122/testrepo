#！/usr/bin/env python3
# coding:utf-8

from core import src
from interface import admin_interface
# 添加用户
def add_user():
    src.register()


# 修改用户额度
def change_balance():
    while 1:
        # 1）输入需要修改额度的用户
        change_user = input('请输入需要修改额度的用户').strip()
        # 2）修改用户的额度
        money = input('请输入修改用户的额度').strip()
        if not money.isdigit():
            continue
        # 3）调用额度修改接口
        flag,msg = admin_interface.change_balance_interface(
            change_user,money
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)

# 冻结用户
def lock_user():
    while 1:
        # 1）输入冻结的用户名
        change_user = input('请输入需要冻结的用户名：').strip()
        flag,msg = admin_interface.lock_user_interface(
            change_user
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)

# 管理员功能字典
admin_func = {
    '1': add_user,
    '2': change_balance,
    '3': lock_user
}

def admin_run():
    while 1:
        print('''
        1. 添加账户
        2. 修改额度
        3. 冻结账户
        4. 退出管理员
        ''')
        choice = input('请输入管理员功能编号：').strip()
        if choice == '4':
            print('已退出管理员页面！')
            break
        if choice not in admin_func:
            print('请输入正确的功能编号！')
            continue

        admin_func.get(choice)()











"""
@version:1.0
@author:wanghonghao
@file:admin.py
@time:2021/5/6 1:52
"""