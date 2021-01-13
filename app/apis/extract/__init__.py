# !/usr/bin/env python
# coding:utf-8
# @Time    : 2021/01/13 10:50 上午
# @Name    : __init__.py.py
# @Desc    :


"""
原理：
api.add_resource(resource, url)
1、将创建的接口类注册到app中
"""

from flask import Blueprint

extract = Blueprint("extract", __name__, static_folder='../static/extract', static_url_path='../static/extract')

# 对象
user = {
    # 路由
    "DEFAULT_RESOURCE": (

    ),
    # 蓝本
    "ALL_BLUEPRINT": (
        extract,
    ),
}

__all__ = ['user', "extract"]
