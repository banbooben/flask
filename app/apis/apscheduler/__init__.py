#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:36 下午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : __init__.py.py
# @desc    :

from flask import Blueprint
from .ap_scheduler import APSchedulerResource, APSchedulerDeleteResource

bp_scheduler = Blueprint("bp_scheduler", __name__, static_folder='../static/scheduler',
                         static_url_path='../static/scheduler')

# 是否启动本模块
enable = True

# 对象
registry = {
    # 路由
    "RESOURCE": (
        (APSchedulerResource, "/api/scheduler"),
        (APSchedulerDeleteResource, "/api/scheduler/<string:job_id>"),

    ),
    # 蓝本
    "BLUEPRINT": (
        bp_scheduler,
    ),
}
