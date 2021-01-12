# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Name    : __init__.py.py
# @Desc    :


from flask import Flask
from flask_cors import CORS
from flask_log_request_id import RequestID, current_request_id

from apis import register_resource_and_blueprint
from config.server_conf import config
# from route import route_extensions

from initialization.extensions import config_extensions
from initialization.logger_process import logger
from initialization.error_process import init_error


# from .extensions.my_logger.extensions_log import handler
# from config.myLog import logger


def init_app(config_name='default'):
    flask_app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/')

    # 配置基类
    if config_name not in config:
        config_name = 'default'
    flask_app.config.from_object(config[config_name])

    # 设置跨域
    flask_app.config["JSON_AS_ASCII"] = False
    CORS(flask_app, supports_credentials=True)

    # 配置蓝本路由、api接口
    register_resource_and_blueprint(flask_app)

    # 配置日志
    flask_app.logger.addHandler(logger)

    # 配置扩展
    config_extensions(flask_app)

    # 未知
    RequestID(flask_app)

    init_error(flask_app)
    # # 配置蓝本路由
    # route_extensions(flask_app)
    #
    # # 配置api接口
    # config_resource(flask_app)

    return flask_app

# app_conf = {"http_host": HTTP_HOST, "http_port": HTTP_PORT}
