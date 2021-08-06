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
from initialization.logger_process import logger
from flask import current_app


class TestResource(BaseResource):

    def get(self):
        print(current_app.logger is logger)
        print(logger.level)
        logger.debug("test")
        logger.info("info")
        return self.response(code=200, message="请求成功")





