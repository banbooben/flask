#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/2 4:04 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : __init__.py.py
# @desc    :

"""
原理：
api.add_resource(resource, url)
1、将创建的接口类注册到app中
"""

from flask import Blueprint
from .test import TestResource

bp_test = Blueprint("bp_test", __name__, static_folder='../static/extract', static_url_path='../static/extract')

# 是否启动本模块
enable = True

# 对象
registry = {
    # 路由
    "RESOURCE": (
        (TestResource, "/v1/test"),

    ),
    # 蓝本
    "BLUEPRINT": (
        bp_test,
    ),
}

