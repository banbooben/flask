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
from application.initialization.resource_process import BaseResource


class CustomBlueprintBase(object):

    def __init__(self):
        self._enable = True
        self._bp = self.init_blueprint()
        self._resource = self.init_resource()

    @abc.abstractmethod
    def init_blueprint(self) -> Blueprint:
        pass

    @abc.abstractmethod
    def init_resource(self) -> Tuple[Tuple[BaseResource, str], ...]:
        pass

    # @classmethod
    @property
    def blueprint(self):
        return self._bp

    @property
    def resource(self):
        return self._resource

    def set_enable(self, flag: [True, False]):
        self._enable = flag
