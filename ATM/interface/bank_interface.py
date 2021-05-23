#！/usr/bin/env python3
# coding:utf-8
'''
银行业务相关接口
'''

# import time
from DB import db_handler
from lib import common

bank_logger = common.get_logger(log_type='bank')

# 提现接口（手续费5%）
def withdraw_interface(username,money):

    # 1）先获取用户字典
    user_dic = db_handler.select(username)
    # 校验用户的钱是否足够
    balance = int(user_dic.get('balance'))
    # 本金+手续费
    money2 = int(money) * 1.05  # ---> float

    # 判断用户金额是否足够
    if balance >= money2:
        # 2）修改用户字典中的金额
        balance -= money2
        user_dic['balance'] = balance

        # 3）记录流水
        flow = f'用户{username}提现金额：{money}元成功，手续费为：{money2-float(money)}元'
        # flow1 = time.strftime('%Y-%m-%d %X') + flow
        user_dic['flow'].append(flow)

        # 4）再保存数据，或更新数据
        db_handler.save(user_dic)

        bank_logger.info(flow)

        return True,flow
    return False,'提现金额不足，请重试！'

# 还款接口
def repay_interface(username,money):
    # 1）获取用户的金额
    # 2）给用户的金额做加前的操作

    # 1. 过去用户字典
    user_dic = db_handler.select(username)
    # 2.直接做加前操作
    user_dic['balance'] += money
    # 3.记录流水
    flow = f'用户：{username}还款{money}成功！当前额度为：{user_dic["balance"]}'
    user_dic['flow'].append(flow)
    # 4.调用数据处理层，将修改后的数据更新
    db_handler.save(user_dic)
    bank_logger.info(flow)
    return True,flow

# 转账接口
def transfer_interface(login_user,to_user,money):
    '''
    1.获取当前用户
    2.获取转账目标用户
    3.获取转账金额
    '''
    # 1）获取当前用户字典
    login_user_dic = db_handler.select(login_user)
    # 2）获取目标用户字典
    to_user_dic = db_handler.select(to_user)
    # 3）判断目标用户是否存在
    if not to_user_dic:
        return False,f'{to_user}用户不存在！'
    # 4）若用户存在，则判断 当前用户的转账金额是否足够
    if login_user_dic['balance'] >= money:
        # 5）若足够，给当前用户减钱操作，并给目标用户加钱操作
        login_user_dic['balance'] -= money
        to_user_dic['balance'] += money
        # 5.1）记录当前用户和目标用户的流水
        login_user_flow = f'用户{login_user}给用户{to_user}转账{money}元成功！'
        login_user_dic['flow'].append(login_user_flow)

        to_user_flow = f'用户{to_user}接收到用户{login_user}转账{money}元成功！'
        to_user_dic['flow'].append(to_user_flow)

        # 6）调用数据处理层save功能，保存用户数据
        # 6.1）保存当前用户数据
        db_handler.save(login_user_dic)
        # 6.2）保存目标用户数据
        db_handler.save(to_user_dic)

        bank_logger.info(login_user_flow)

        return True,login_user_flow
    return False,'当前账号余额不足！'

# 查看流水接口
def check_flow_interface(login_user):
    user_dic = db_handler.select(login_user)
    return user_dic.get('flow')

# 支付接口
def pay_interface(login_user,cost):
    user_dic = db_handler.select(login_user)

    # 判断用户金额是否足够
    if user_dic.get('balance') >= cost:
        user_dic['balance'] -= cost

        # 记录消费流水
        flow = f'用户{login_user}消费金额{cost}元'
        user_dic['flow'].append(flow)

        db_handler.save(user_dic)
    # return True or False交给shopping_interface处理的，不是给用户的
        bank_logger.info(flow)
        return True
    return False



"""
@version:1.0
@author:wanghonghao
@file:bank_interface.py
@time:2021/5/2 21:56
"""