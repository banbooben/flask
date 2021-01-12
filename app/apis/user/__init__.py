# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/27 12:00 上午
# @Name    : __init__.py.py
# @Desc    :


"""
原理：
api.add_resource(resource, url)
1、将创建的接口类注册到app中
"""

from flask import Blueprint

bp_user = Blueprint("user", __name__, static_folder='../static/aria', static_url_path='../static/aria')

# 对象
user = {
    # 路由
    "DEFAULT_RESOURCE": (

    ),
    # 蓝本
    "ALL_BLUEPRINT": (
        bp_user,
    ),
}

__all__ = ['user', "bp_user"]
