#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 17:45
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    : 
# @File    : base_resource_process.py
# @desc    :

from flask_restful import Resource
from flask import request


class BaseResource(Resource):

    def data(self):
        return request.params

    def files(self):
        return request.files

    def response(self, message=None, code=200, data=None, *args, **kwargs):
        message = message or ""
        data = data or {}

        resp = {
            "message": message,
            "code": code,
            'data': data,
            "history_id": request.request_id
        }

        resp.update(kwargs)
        return resp

