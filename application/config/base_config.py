#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2022-04-27 13:04:48
# @LastEditTime: 2022-04-27 13:04:48
# @FilePath: /flask/application/config/base_config.py

import os
import random
# from flask_app.common.common_conf import get_databases_url
from pathlib import Path
import multiprocessing


class BaseConfig(object):
    # app基础配置
    # 密钥
    PROJECT_NAME = "flask_app"
    SECRET_KEY = ''.join(
        random.sample('zyxwvutsrqponmlkjihgfedcba!@#$%^&*', 32)).encode()

    # 服务运行端口绑定
    # BIND = os.getenv("BIND", "0.0.0.0:5000")
    WORK_NUMS = os.getenv("WORK_NUMS", multiprocessing.cpu_count())

    # app静态资源路径
    TEMPLATE_FOLDER = Path('/flask_app/templates').as_posix()
    STATIC_FOLDER = Path('/flask_app/static').as_posix()
    # STATIC_URL_PATH = '/'

    # 日志配置存储位置
    LOG_DIR = (Path.cwd() / 'logs').as_posix()
    LOG_LEVEL = "INFO"
    LOG_FILE_NAME = os.getenv("LOG_FILE_NAME", 'root.log')

    # 上传文件存储位置
    # UPLOAD_PATH = (Path.cwd() / 'flask_app/static').as_posix()
    # UPLOAD_PATH = Path('/flask_app/static').as_posix()
    # 上传文件允许格式
    ALLOWED_EXTENSIONS = tuple(["pdf", "PDF", "doc", "docx", "txt"])

    JWT_URL_WHITE_LIST = {
        ('/', 'GET'),
    }
