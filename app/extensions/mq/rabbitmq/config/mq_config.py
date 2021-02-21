#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/8 17:48
# @Author  : shangyameng
# @Email   : shangyameng@datagrand.com
# @Site    : 
# @File    : mq_config.py
# @desc    :

import os
import json


class BaseConfig(object):
    """基础的简单模式"""

    # 账号密码
    username = "guest"
    password = "guest"

    # 主机端口
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "5673")

    # 是否开启消息手动确认机制, 默认是自动确认机制
    ack = True

    # 消息是否持久化
    persist = True

    # 交换机名称
    exchange = ""

    # 交换机类型
    exchange_type = ""


class WorkingConfig(BaseConfig):
    """工作模式"""
    pass


class ReleaseSubscriptionConfig(BaseConfig):
    """发布订阅模式"""
    pass


class RoutingConfig(BaseConfig):
    """路由模式"""
    pass


class ThemeConfig(BaseConfig):
    """主题模式"""
    pass


class RPCConfig(BaseConfig):
    """RPC模式"""
    pass


config = {
    "default": BaseConfig,
    "work": WorkingConfig,
    "release_subscription": ReleaseSubscriptionConfig,
    "rout": RoutingConfig,
    "theme": ThemeConfig,
    "rpc": RPCConfig,
}


# global current_config
current_environment = os.getenv("ENVIRONMENT", "default")
current_config = config.get(current_environment)
