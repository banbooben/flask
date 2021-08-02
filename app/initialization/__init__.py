# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Name    : __init__.py.py
# @Desc    :

from flask import Flask
from flask_cors import CORS
from flask_log_request_id import RequestID

from apis import register_resource_and_blueprint
from config.server_conf import current_config

from initialization.extensions import config_extensions
from initialization.application import logger
from initialization.error_process import init_error
from initialization.request_process import init_hook_function, Request


def init_app():

    # 初始化app
    flask_app = Flask(__name__,
                      template_folder=current_config.TEMPLATE_FOLDER,
                      static_folder=current_config.STATIC_FOLDER,
                      static_url_path=current_config.STATIC_URL_PATH)

    # 配置基类
    flask_app.config.from_object(current_config)

    # 设置跨域
    flask_app.config["JSON_AS_ASCII"] = False
    CORS(flask_app, supports_credentials=True)

    # 重写request，并添加相关方法
    flask_app.request_class = Request

    # 注册全局错误
    init_error(flask_app)

    # 注册钩子函数
    init_hook_function(flask_app)

    # 配置蓝本路由、api接口
    register_resource_and_blueprint(flask_app)

    # 配置扩展
    config_extensions(flask_app)

    # 注册获取请求ID，供日志使用
    RequestID(flask_app)

    return flask_app
