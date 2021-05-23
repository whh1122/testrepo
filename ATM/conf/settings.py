#！/usr/bin/env python3
# coding:utf-8
'''
存放配置信息
'''

import os

# 获取项目根目录路径
BASE_PATH = os.path.dirname(
    os.path.dirname(__file__)
)

# Windows平台下
BASE_PATH = BASE_PATH.replace('/','\\')
# print(BASE_PATH)  # 测试Windows、Linux系统下文件目录显示形式

# 获取user_data文件夹目录路径
USER_DATA_PATH = os.path.join(
    BASE_PATH,'DB','user_data'
)
# 解决Windows平台os.path.join拼接的地址反斜杠错误
# Linux平台下
# USER_DATA_PATH = USER_DATA_PATH.replace('\\','/')

# print(USER_DATA_PATH)  # 测试Windows、Linux系统下文件目录显示形式


'''
logging配置
'''


standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

test_format = '[%(asctime)s] %(message)s'


# BASE_PATH = os.path.dirname(os.path.dirname(__file__))
logfile_dir = os.path.join(BASE_PATH,'log')
# print(logfile_dir)
logfile_name = 'atm.log'

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)
# log文件的全路径

logfile_path = os.path.join(logfile_dir,logfile_name)
# print(logfile_path)
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'test': {
            'format': test_format
        },
    },
    'filters': {},
    'handlers': {
        #打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        #打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'formatter': 'standard',
            # 可以定制日志文件路径
            # BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # log文件的目录
            # LOG_PATH = os.path.join(BASE_DIR,'a1.log')
            'filename': logfile_path,  # 日志文件
            'maxBytes': 1024*1024*5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        'other': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',  # 保存到文件
            'formatter': 'test',
            'filename': logfile_path,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        #logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG', # loggers(第一层日志级别关限制)--->handlers(第二层日志级别关卡限制)
            'propagate': True,  # 默认为True，向上（更高level的logger）传递，通常设置为False即可，否则会一份日志向上层层传递
        },
        'xxx': {
            'handlers': ['other',],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}








"""
@version:1.0
@author:wanghonghao
@file:settings.py
@time:2021/5/2 21:51
"""