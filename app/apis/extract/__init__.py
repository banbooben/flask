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
from .extract_view import ExtractView

bp_extract = Blueprint("bp_extract", __name__, static_folder='../static/extract', static_url_path='../static/extract')

# 对象
extract = {
    # 路由
    "DEFAULT_RESOURCE": (
        (ExtractView, "/api/extract"),

    ),
    # 蓝本
    "ALL_BLUEPRINT": (
        bp_extract,
    ),
}

__all__ = ['extract', "bp_extract"]
