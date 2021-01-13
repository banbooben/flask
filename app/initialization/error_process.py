# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Name    : error_process.py.py
# @Desc    :


# from utils.error_exception import APIException
from flask import jsonify, request
from utils.exception_process import APIException, ExtractException


def init_error(app):
    @app.errorhandler(APIException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(ExtractException)
    def extract_error_handle(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(405)
    def extract_error_handle(error):
        return {"code": 405, "message": "Method Not Allowed", "status": "fail", "id": request.request_id}

    @app.errorhandler(404)
    def extract_error_handle(error):
        return {"code": 404, "message": "The requested URL was not found on the server", "status": "fail",
                "id": request.request_id}


def register_blueprint_error(blueprint):
    @blueprint.app_errorhandler(APIException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @blueprint.app_errorhandler(ExtractException)
    def extract_error_handle(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @blueprint.app_errorhandler(405)
    def extract_error_handle(error):
        return {"code": 405, "message": "Method Not Allowed", "status": "fail", "id": request.request_id}

    @blueprint.app_errorhandler(404)
    def extract_error_handle(error):
        return {"code": 404, "message": "The requested URL was not found on the server", "status": "fail",
                "id": request.request_id}
