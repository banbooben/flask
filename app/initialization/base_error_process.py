# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Name    : base_error_process.py.py
# @Desc    :

import json
from flask import jsonify, request

from werkzeug.exceptions import HTTPException
from initialization.application import logger


class ExceptionBase(Exception):
    def __init__(self, message, code=None, payload=None):
        super().__init__()
        self.message = message
        self.code = code if code else 400
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv.update(self.get_request_id())
        rv['message'] = self.message
        rv['code'] = self.code
        rv['data'] = {}
        logger.error(json.dumps(rv))
        return rv

    @staticmethod
    def get_request_id():
        from flask import request
        request_id = None

        try:
            request_id = request.request_id
        finally:
            return {"request_id": request_id}


class APIException(ExceptionBase):
    ...


class FileException(ExceptionBase):
    def __init__(self, message="", code=None, payload=None):
        super().__init__(message, code, payload)
        self.set_default_message_by_code()

    def set_default_message_by_code(self):

        if self.code == "F001":
            if not self.message:
                self.message = "缺少文件！"


class ExtractException(ExceptionBase):
    status_code = 400

    def __init__(self, message="", code=None, payload=None):
        super().__init__(self)
        self.message = message
        self.payload = payload
        self.code = code
        self.set_default_code()

    def to_dict(self):
        rv = dict(self.payload or ())
        rv.update(self.get_request_id())
        rv['message'] = self.message
        rv['code'] = self.code if self.code else self.status_code
        rv['status'] = "FAIL"
        rv['data'] = {}
        logger.error(json.dumps(rv))
        return rv

    def set_default_code(self):

        if self.code == "E01":
            if not self.message:
                self.message = "缺少文件！"
        # elif self.code == "E02":
        #     if not self.message:
        #         self.message = "上传文件类型错误"
        # elif self.code == "E03":
        #     if not self.message:
        #         self.message = "文件读写、保存失败，检查文件是否可读、可写"
        # elif self.code == "E04":
        #     if not self.message:
        #         self.message = "系统内部错误"
        # elif self.code == "E05":
        #     if not self.message:
        #         self.message = "PDF文件解析失败"
        # elif self.code == "E06":
        #     if not self.message:
        #         self.message = "word文件解析失败"
        # elif self.code == "E07":
        #     if not self.message:
        #         self.message = "文档解析失败"


def init_error(app):
    @app.errorhandler(APIException)
    @app.errorhandler(FileException)
    @app.errorhandler(ExtractException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.code if error.code.isdigit() else 400
        return response

    # @app.errorhandler(ExtractException)
    # def extract_error_handle(error):
    #     response = jsonify(error.to_dict())
    #     response.status_code = error.status_code
    #     return response
    #
    # @app.errorhandler(FileException)
    # def file_error_handle(error):
    #     response = jsonify(error.to_dict())
    #     response.status_code = error.status_code
    #     return response

    @app.errorhandler(405)
    def extract_error_handle(error):
        return {"code": 405, "message": "Method Not Allowed", "status": "FAIL", "id": request.request_id}

    @app.errorhandler(404)
    def extract_error_handle(error):
        return {"code": 404, "message": "The requested URL was not found on the server", "status": "FAIL",
                "id": request.request_id}

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": "E04",
            "id": request.request_id,
            "message": e.description,
            "status": "FAIL",
            "name": e.name,
        })
        response.content_type = "application/json"
        return response

    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     """Return JSON instead of HTML for HTTP errors."""
    #     # start with the correct headers and status code from the error
    #     response = e.get_response()
    #     # replace the body with JSON
    #     response.data = json.dumps({
    #         "code": "E04",
    #         "id": request.request_id,
    #         "message": e.description,
    #         "status": "FAIL",
    #         "name": e.name,
    #     })
    #     response.content_type = "application/json"
    #     return response


def register_blueprint_error(blueprint):
    @blueprint.app_errorhandler(APIException)
    @blueprint.app_errorhandler(FileException)
    @blueprint.app_errorhandler(ExtractException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.code if error.code.isdigit() else 400
        return response

    # @blueprint.app_errorhandler(ExtractException)
    # def extract_error_handle(error):
    #     response = jsonify(error.to_dict())
    #     response.status_code = error.status_code
    #     return response

    @blueprint.app_errorhandler(405)
    def extract_error_handle(error):
        return {"code": 405, "message": "Method Not Allowed", "status": "FAIL", "id": request.request_id}

    @blueprint.app_errorhandler(404)
    def extract_error_handle(error):
        return {"code": 404, "message": "The requested URL was not found on the server", "status": "FAIL",
                "id": request.request_id}
