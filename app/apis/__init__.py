# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Contact : shangyameng
# @Name    : __init__.py.py
# @Desc    :


from flask_restful import Api as _Api

from initialization.error_process import register_blueprint_error
from initialization.request_process import init_bp_hook_function
from initialization.logger_process_class import logger

import os

import importlib


def load_all_resource_and_blueprint():
    all_modules = []
    default_dirs = "apis"
    for root, dirs, files in os.walk(default_dirs):
        for _dir in dirs:
            if root in ["apis"]:
                break
            elif _dir in ["__pycache__"]:
                continue
            abs_file_path = os.path.join(root, _dir)
            module = importlib.import_module(abs_file_path.replace("/", "."))
            importlib.reload(module)
            try:
                registry = getattr(module, 'registry')
                all_modules.append(registry)
            except Exception as e:
                logger.exception(e)
    return all_modules


class Api(_Api):
    def handle_error(self, e):
        raise e


def register_resource_and_blueprint(app):
    api = Api(app)
    all_resource_and_blueprint = load_all_resource_and_blueprint()
    for api_obj in all_resource_and_blueprint:

        for api_info in api_obj.get("RESOURCE", ()):
            resource, url = api_info[0], api_info[1]
            api.add_resource(resource, url)

        for bp in api_obj.get("BLUEPRINT", ()):
            app.register_blueprint(bp, url_prefix="/{}".format(bp.name))
            register_blueprint_error(bp)
            init_bp_hook_function(bp)
