#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 19:53
# @Author  : shangyameng
# @Email   : shangyameng@datagrand.com
# @Site    : 
# @File    : exception_process.py
# @desc    :


class APIException(Exception):

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code if status_code else 500
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['code'] = self.status_code
        rv['data'] = {}
        return rv


class ExtractException(Exception):
    status_code = 400

    def __init__(self, message="", code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
        self.code = code
        self.set_default_code()

    def to_dict(self):
        rv = dict(self.payload or ())
        rv.update(self.get_extract_id())
        rv['message'] = self.message
        rv['code'] = self.code if self.code else self.status_code
        rv['status'] = "fail"
        rv['data'] = {}
        return rv

    def set_default_code(self):

        if self.code == "E01":
            self.message = "文档类型不合法"
        elif self.code == "E02":
            self.message = "report_id不合法"
        elif self.code == "E03":
            self.message = "文件类型错误"
        elif self.code == "E04":
            self.message = "文件读取失败"
        elif self.code == "E05":
            self.message = "文档转化失败"
        elif self.code == "E06":
            self.message = "抽取服务调用失败"
        elif self.code == "E07":
            self.message = "数据写入json文件失败"

    @staticmethod
    def get_extract_id():
        from flask import request

        report_id = request.params.get("report_id", None)
        if report_id:
            return {"id": report_id}
        return {}
