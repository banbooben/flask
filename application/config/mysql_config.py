#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2022-04-27 13:06:17
# @LastEditTime: 2022-04-27 13:06:18
# @FilePath: /flask/application/config/mysql_config.py

import os
from .base_config import BaseConfig


# 配置基类
class Config(BaseConfig):
    # 是否使用链接池
    USE_DB_POOL = True
    """ Flask-JWT配置 """
    SSO_LOGIGN = os.getenv('SSO_LOGIGN', True)  # 是否支持单点登录 True:支持，False:不支持
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 60 * 60 * 24)
    LOGIN_KEY = os.getenv('LOGIN_KEY', "lk_")
    TOKEN_LIFETIME = 1800  # token有效期

    # 数据库的配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 配置自动提交
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否显示错误信息
    SQLALCHEMY_ECHO = False  # 调试模式显示错误信息
    SQLALCHEMY_POOL_SIZE = 20  # 链接池数量
    SQLALCHEMY_POOL_MAX_OVERFLOW = 5  # 超出后，可以创建的链接数
    SQLALCHEMY_POOL_PRE_PING = True  # 每次取出一个连接时，会发送一个select 1来检查连接是否有效
    SQLALCHEMY_POOL_TIMEOUT = 30  # 链接超时时间
    SQLALCHEMY_POOL_RECYCLE = os.getenv("SQLALCHEMY_POOL_RECYCLE", 8 * 60)  # 表示连接在给定时间之后会被回收，不能超过8小时

    MAX_PAGE_SIZE = 1000000

    # 数据库基础配置
    DATABASES_USER = os.getenv('MYSQL_PASSWORD', 'root')
    DATABASES_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    DATABASES_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    DATABASES_PORT = os.getenv('MYSQL_PORT', 212330690)
    DATABASES_DATABASES = os.getenv('MYSQL_DATABASES', "smbc")
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASES_USER}:{DATABASES_PASSWORD}@{DATABASES_HOST}:{DATABASES_PORT}/{DATABASES_DATABASES}'

    REDIS_CONF = {
        "CACHE_TYPE": os.getenv('CACHE_TYPE', 'redis'),
        "REDIS_HOST": os.getenv('REDIS_HOST', 'redis'),
        "REDIS_PORT": os.getenv('REDIS_PORT', 6379),
        "REDIS_DB": os.getenv('REDIS_DB', 3),
        "REDIS_PASSWORD": os.getenv('REDIS_PASSWORD', ''),
        "DECODE_RESPONSES": os.getenv('DECODE_RESPONSES', "True"),
    }

    SQLALCHEMY_BINDS = {
        'base': SQLALCHEMY_DATABASE_URI,
    }
