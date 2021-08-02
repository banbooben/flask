#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/2 4:05 下午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : test.py
# @desc    :

from common.decorators import Decorator
from initialization.resource_process import BaseResource


class TestResource(BaseResource):

    def get(self):

        return self.response(code=200, message="请求成功")





