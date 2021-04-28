#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-04-08 22:56:46
# @LastEditTime: 2021-04-12 14:19:54
# @FilePath: /app/config/server_conf.py

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

    conf = {
        "default": "DEBUG",
        "test": "DEBUG",
        "product": "INFO",
    }

    # 日志配置存储位置
    LOG_DIR = (Path.cwd() / 'logs').as_posix()
    LOG_LEVEL = "default"

    # 上传文件存储位置
    UPLOAD_PATH = (Path.cwd() / 'static/upload').as_posix()
    # 上传文件允许格式
    ALLOWED_EXTENSIONS = set(["pdf", "PDF", "doc", "docx"])

    # 服务器文件路径
    SERVER_UPLOAD_PATH = "/share_data/gtja_api/upload"

    # app静态资源路径
    TEMPLATE_FOLDER = '../templates'
    STATIC_FOLDER = '../static'
    STATIC_URL_PATH = '/'

    # 路由白名单
    URL_WHITE_LIST = {
        '/': ['GET'],
    }

    # 服务运行端口绑定
    BIND = os.getenv("BIND", "0.0.0.0:5000")
    WORK_NUMS = os.getenv("WORK_NUMS", multiprocessing.cpu_count())

    # 数据库基础配置
    DATABASES = {
        'USER': os.getenv('MYSQL_PASSWORD', 'root'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'shang.666'),
        'HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.getenv('MYSQL_PORT', 33061),
        'DATABASES': os.getenv('MYSQL_DATABASES', "seeds")
    }

    SQLALCHEMY_DATABASE_URI = get_databases_url(DATABASES)

    # 缓存
    REDIS_CONF = {
        "CACHE_TYPE": os.getenv('CACHE_TYPE', 'redis'),
        "REDIS_HOST": os.getenv('REDIS_HOST', '127.0.0.1'),
        "REDIS_PORT": os.getenv('REDIS_PORT', 6379),
        "REDIS_DB": os.getenv('REDIS_DB', 0),
        "REDIS_PASSWORD": os.getenv('REDIS_PASSWORD', ''),
        "DECODE_RESPONSES": os.getenv('DECODE_RESPONSES', "True"),
    }


# 生产环境配置
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

    # # 路由白名单
    # URL_WHITE_LIST = {
    #     '/': ['GET'],
    # }


# 测试环境配置
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

    # # 路由白名单
    # URL_WHITE_LIST = {
    #     '/': ['GET'],
    # }


# 本地环境配置
class LocalConfig(Config):
    # 缓存
    REDIS_CONF = {
        "CACHE_TYPE": os.getenv('CACHE_TYPE', 'redis'),
        "REDIS_HOST": os.getenv('REDIS_HOST', '100.100.20.155'),
        "REDIS_PORT": os.getenv('REDIS_PORT', 6379),
        "REDIS_DB": os.getenv('REDIS_DB', 0),
        "REDIS_PASSWORD": os.getenv('REDIS_PASSWORD', ''),
        "DECODE_RESPONSES": os.getenv('DECODE_RESPONSES', "True"),
    }

    # 日志等级设置
    LOG_LEVEL = "test"

    # # 路由白名单
    # URL_WHITE_LIST = {
    #     '/': ['GET'],
    # }


config = {
    'default': LocalConfig,
    'test': TestConfig,
    'product': ProductConfig,
}

# global current_config
current_environment = os.getenv("ENVIRONMENT", "default")
current_config = config.get(current_environment, "test")
