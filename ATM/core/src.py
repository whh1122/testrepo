#！/usr/bin/env python3
# coding:utf-8
'''
用户视图层
'''

from interface import user_interface
from interface import bank_interface
from interface import shop_interface

from lib import common


# 全局变量，记录用户是否已登录
login_user = None

# 面条版
'''
def register():
    while 1:
        # 1) 让用户输入用户名和密码进行校验
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        re_password = input('请确认密码：').strip()

        # 小的逻辑处理：如两次密码是否一致
        if password == re_password:
            import json,os
            from conf import settings
            user_path = os.path.join(
                settings.USER_DATA_PATH,f'{username}.json'
            )
            # 2） 查看用户是否存在
            # 2.1) 若不存在，则让用户重新输入
            if os.path.exists(user_path):
                print('请重新输入')

                with open(user_path,mode='r',encoding='utf-8') as f:
                    user_dic = json.load(f)

                if user_dic:
                    print('用户已存在，请重新输入')
                    continue

            # 3） 若用户存在，则让用户重新输入
            # 4） 若用户不存在，则保存用户数据
            # 4.1） 组织用户的数据字典信息
            user_dic = {
                'username':username,
                'password':password,
                'balance':15000,
                # 用于记录用户流水的列表
                'flow':[],
                # 用于记录用户购物车
                'shop_car':{},
                # locked：用于记录用户是否被冻结，False：未冻结，Ture：已被冻结
                'locked':False

            }



            # 存不是目的，目的是为了更好的取数据
            # 文件名：用户名.json，如egon.json  tank.json
            # 4.2） 拼接用户的json文件路径
            user_path = os.path.join(
                settings.USER_DATA_PATH,f'{username}.json'
            )

            # user_path = user_path.replace('/','\\') # 测试代码，勿启用
            # print(user_path)

            with open(user_path,mode='w',encoding='utf-8') as f:
                json.dump(user_dic,f,ensure_ascii=False)  # ensure_ascii=False可以显示中文
'''

# 分层版
# 1.注册功能
def register():
    while 1:
        # 1) 让用户输入用户名和密码进行校验
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        re_password = input('请确认密码：').strip()

        # 小的逻辑处理：如两次密码是否一致
        if password == re_password:
            # 2) 调用接口层的注册接口，将用户名与密码交给接口层进行处理

            # res ---> (False,'用户名已存在！') 元组
            # flag,mag --->  (False,'用户名已存在！') 解压赋值

            # (True,f'{username}注册成功！')  (False,'用户名已存在！')
            flag,msg = user_interface.register_interface(
                username,password
            )
            # 3）根据flag判断用户注册是否成功，用于控制break的结束
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print('两次输入密码不一致，请重新输入')


# 2.登录功能
def login():
    # 登录视图
    while 1:
        # 1）让用户输入用户名和密码
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()

        # 2）调用接口层，将数据传给登录接口
        # (True,f'用户：{username}登录成功！') or
        # (False,'密码错误！') or
        # (False,'用户不存在，请重新输入！')
        flag,msg = user_interface.login_interface(
            username,password
        )
        if flag:
            print(msg)
            global login_user
            login_user = username
            break
        else:
            print(msg)




# 3.查看余额
@common.login_auth
def check_balance():
    # 1）直接调用查看余额接口，获取用户余额
    balance = user_interface.check_bal_interface(
        login_user
    )
    print(f'用户：{login_user}的账户余额为：{balance}元')

# 4.提现功能
@common.login_auth
def withdraw():
    while 1:
        # 1) 让用户输入提现金额
        input_money = input('请输入提现金额：').strip()

        # 2）判断用户输入的金额是否是数字
        if not input_money.isdigit():
            print('请重新输入')
            continue

        # 3）用户提现金额，将提现的金额交付给接口层来处理
        input_money = int(input_money)
        flag,msg = bank_interface.withdraw_interface(
            login_user,input_money
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)







# 5.还款功能
@common.login_auth
def repay():
    while 1:
        # 1） 让用户输入还款金额
        input_money = input('请输入还款金额：').strip()
        # 2) 判断用户输入的金额是否为数字
        if not input_money.isdigit():
            print('请输入正确的金额！')
            continue
        input_money = int(input_money)
        # 3) 判断用户输入金额大于0
        if input_money > 0:
            # 4） 调用还款接口
            flag,msg = bank_interface.repay_interface(
                login_user,input_money
            )
            if flag:
                print(msg)
                break
        else:
            print('输入的金额不能小于0！')


# 6.转账功能
@common.login_auth
def transfer():
    '''
    1.接收用户输入的转账金额
    2.接收用户输入的转账
    '''
    while 1:
        # 1）让用户输入转装用户和金额
        to_user = input('请输入转账目标用户：').strip()
        money = input('请输入转账金额：').strip()

        # 2）判断用户输入的金额是否为数字或>0
        if not money.isdigit():
            print('请输入正确的金额！')
            continue

        money = int(money)
        if money > 0:
            # 3）调用转账接口
            flag,msg = bank_interface.transfer_interface(
                login_user,to_user,money
            )
            if flag:
                print(msg)
            else:
                print(msg)
            break
        else:
            print('请输入正确的金额！')


# 7.查看流水
@common.login_auth
def check_flow():
    # 直接查看流水接口
    flow_list = bank_interface.check_flow_interface(
        login_user
    )

    if flow_list:
        for flow in flow_list:
            print(flow)
    else:
        print('当前用户未产生流水！')

# 8.购物功能
@common.login_auth
def shopping():
    # 创建一个商品列表，（优化则从文件读取商品数据）
    # 可以是字典套字典，也可以是列表套列表
    goods_list = [
        ['mate40',4500],
        ['mini5',2099],
        ['小龙虾',120],
        ['heytea',25],
        ['Q5',450000],
        ['airpods',888],
        ['xps15',9000]
    ]

    # 初始化当前购物车
    shopping_car = {}  # {'商品名称':['单价','数量']}

    while 1:
        # 1）打印商品信息，让用户选择
        # 枚举：enumerate(可迭代对象) ---> (可迭代对象的索引，索引对应的值)
        # 枚举：enumerate(可迭代对象) ---> (0,['mate40',4500])
        print('========欢迎来到有趣用品商城=========')
        for index,goods in enumerate(goods_list):
            goods_name,goods_price = goods
            print(
                f'商品编号：{index}',
                f'名称：{goods_name}',
                f'单价：{goods_price}'
            )
        print('=========24小时无人自助服务=========')
        # 2）让用户根据商品编号进行选择
        choice = input('请输入商品编号（是否结账输入y or n）：').strip()

        # 输入y进入支付结算功能
        if choice == 'y' or choice == 'Y':
            if not shopping_car:
                print('购物是空的，不能支付，请重新输入！')
                continue

            # 调用和支付接口
            flag,msg = shop_interface.shopping_interface(
                login_user,shopping_car
            )
            if flag:
                print(msg)
                break
            else:
                print(msg)

        # 输入n添加购物车
        elif choice == 'n' or choice == 'N':
            # # 判断当前用户是否添加过购物车
            # if not shopping_car:
            #     print('购物是空的，请先添加到购物车')

            # 调用添加购物车接口
            flag,msg = shop_interface.add_shop_car_interface(
                login_user,shopping_car
            )
            if flag:
                print(msg)
                break

        if not choice.isdigit():
            print('请输入正确的商品编号')
            continue
        # 3）判断choice商品是否存在
        choice = int(choice)
        if choice not in range(len(goods_list)):
            print('请输入正确的商品编号')
            continue
        # 4）获取商品名称与单价
        goods_name,goods_price = goods_list[choice]
        # 5）加入购物车
        # 5.1）判断用户的商品是否重复，重复则数量+1，
        if goods_name in shopping_car:
            # 添加商品数量
            shopping_car[goods_name][1] += 1
        else:
            # {'商品名称':['单价','数量']}
            shopping_car[goods_name] = [goods_price,1]

        # shopping_car = {}  # {'商品名称':['单价','数量']}
        print('===当前购物车===')
        for k,v in shopping_car.items():
            price =v[0]
            count = v[1]
            print(
                f'{k}，单价{price}，数量x{count}'
            )
        print('==== END ====')
        # print('当前购物车：',shopping_car)


# 9.查看购物车
@common.login_auth
def check_shop_car():
    car = user_interface.check_car_interface(
        login_user
    )  # ---> {"heytea": [25, 5], "小龙虾": [120, 2], "mate40": [4500, 1]}
    # goodslist_car = []
    print('====购物车====')
    for k,v in car.items():
        count = v[1]
        print(f'{k}，数量x{count}')
    print('==== END ====')

# 10.管理员功能
@common.login_auth
def admin():
    from core import admin
    admin.admin_run()




# 创建函数功能字典
func_dic = {
    '1':register,
    '2':login,
    '3':check_balance,
    '4':withdraw,
    '5':repay,
    '6':transfer,
    '7':check_flow,
    '8':shopping,
    '9':check_shop_car,
    '10':admin
}


# 视图层主程序
def run():
    while 1:
        print('''
        +--- ATM + 购物车 -----+
        |    1. 注册功能       |
        |    2. 登录功能       |
        |    3. 查看余额       |
        |    4. 提现功能       |
        |    5. 还款功能       |
        |    6. 转账功能       |
        |    7. 查看流水       |
        |    8. 购物功能       |
        |    9. 看购物车       |
        |    10.管理功能       |
        +-------- end --------+
        ''')
        choice = input('请输入功能编号： ').strip()

        if choice not in func_dic:
            print('请输入正确的功能编号')
            continue

        func_dic.get(choice)()  # func_dic.get('1')() ---> register()










"""
@version:1.0
@author:wanghonghao
@file:src.py
@time:2021/5/2 21:53
"""