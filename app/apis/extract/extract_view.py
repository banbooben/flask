# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/27 12:00 上午
# @Name    : extract_view.py
# @Desc    :

from flask_restful import Resource
from common.decorators import Decorator


class ExtractView(Resource):

    @Decorator.save_file
    def post(self):
        a = "w"










