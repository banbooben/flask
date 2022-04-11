#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 17:45
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    :
# @File    : resource_process.py
# @desc    :

import abc
from typing import Tuple
from flask_smorest import Blueprint
from application.initialization.resource_process import Api


class CustomBlueprintBase(object):
    _enable = True
    _current_bp = None

    @classmethod
    @abc.abstractmethod
    def init_resource(cls, api_: Api) -> Tuple:
        pass

    @classmethod
    def blueprint(cls):
        return cls._current_bp

    # @property
    @classmethod
    def enable(cls):
        return cls._enable
