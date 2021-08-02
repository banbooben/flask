# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/27 12:00 上午
# @Name    : extract_view.py
# @Desc    :

from flask_restful import Resource
from common.decorators import Decorator
from initialization.resource_process import BaseResource


class ExtractView(BaseResource):

    @Decorator.time_func
    def post(self):
        result = {}
        return self.response(message="ok", result=result)










