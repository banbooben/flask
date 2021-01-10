#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2020-09-01 22:41:33
# @FilePath: /crawlerWeb/crawler_web/config/server_conf.py

import os
from common.common_conf import get_databases_url
from pathlib import Path
import multiprocessing


# 配置基类
class Config(object):
    """
    配置基类
    """
    # 密钥
    SECRET_KEY = 'aliksuydgi/ekjh$gawel;isvnurio'
    # token有效期
    TOKEN_LIFETIME = 1800

    # 数据库的配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 配置自动提交
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否显示错误信息
    SQLALCHEMY_ECHO = True  # 调试模式显示错误信息

    # 日志存储位置
    LOG_DIR = Path.cwd() / 'logs'
    LOG_LEVEL = "default"

    # 路由白名单
    URL_WHITE_LIST = {
        '/': ['GET'],
    }

    # 服务运行端口绑定
    BIND = os.getenv("BIND", "0.0.0.0:5000")
    WORK_NUMS = os.getenv("WORK_NUMS", multiprocessing.cpu_count())


# 环境配置
class ProductConfig(Config):
    DATABASES = {
        'USER': os.getenv('MYSQL_PASSWORD', 'root'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', '123456'),
        'HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.getenv('MYSQL_PORT', 33061),
        'DATABASES': os.getenv('MYSQL_DATABASES', "crawler")
    }

    SQLALCHEMY_DATABASE_URI = get_databases_url(DATABASES)

    # 缓存
    REDIS_CONF = {
        "CACHE_TYPE": os.getenv('CACHE_TYPE', 'redis'),
        "REDIS_HOST": os.getenv('REDIS_HOST', '127.0.0.1'),
        "REDIS_PORT": os.getenv('REDIS_PORT', 6379),
        "REDIS_DB": os.getenv('REDIS_DB', 0),
        "REDIS_PASSWORD": os.getenv('REDIS_PASSWORD', ''),
        "DECODE_RESPONSES": os.getenv('DECODE_RESPONSES', True),
    }

    LOG_LEVEL = "product"

    # 路由白名单
    URL_WHITE_LIST = {
        '/': ['GET'],
    }


# 环境配置
class TestConfig(Config):
    DATABASES = {
        'USER': 'root',
        'PASSWORD': os.getenv('MYSQL_PASSWORD', '123456'),
        'HOST': '127.0.0.1',
        'PORT': '33061',
        'DATABASES': 'gtja'
    }

    SQLALCHEMY_DATABASE_URI = get_databases_url(DATABASES)

    # 缓存
    REDIS_CONF = {
        "CACHE_TYPE": 'redis',
        "REDIS_HOST": '192.168.2.151',
        "REDIS_PORT": 6379,
        "REDIS_DB": 0,
        "REDIS_PASSWORD": '123456',
        "DECODE_RESPONSES": True,
    }

    # 日志等级设置
    LOG_LEVEL = "test"

    # 路由白名单
    URL_WHITE_LIST = {
        '/': ['GET'],
    }


current_environment = "test"
config = {
    'default': TestConfig,
    'test': TestConfig,
    'product': ProductConfig,
}

# global current_config
current_config = config[current_environment]
