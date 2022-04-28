#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:56 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : __init__.py.py
# @desc    :

from .test_jobs import jobs as test_jobs
from .nacos_jobs import jobs as nacos_jobs

all_jobs = [
    test_jobs,
    nacos_jobs,
]

__all__ = ["all_jobs"]
