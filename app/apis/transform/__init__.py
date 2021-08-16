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
from .transform import TransFormResource

bp_transform = Blueprint("bp_transform", __name__, static_folder='../static/transform',
                         static_url_path='../static/transform')

# 是否启动本模块
enable = True

# 对象
registry = {
    # 路由
    "RESOURCE": (
        (TransFormResource, "/v1/transform"),

    ),
    # 蓝本
    "BLUEPRINT": (
        bp_transform,
    ),
}
