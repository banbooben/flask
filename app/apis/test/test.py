#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/2 4:05 下午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : test.py
# @desc    :
from flask import request

from common.decorators import Decorator
from initialization.base_resource_process import BaseResource
from initialization.application import logger

from celery_task.tasks import test_task


class TestResource(BaseResource):

    def get(self):
        logger.debug("test123123")
        logger.info("info123")

        params = request.params
        if params.get("sync", "false") == "true":
            test_task.document_parse.delay()
        else:
            test_task.document_parse()
        return self.response(code=200, message="请求成功")
