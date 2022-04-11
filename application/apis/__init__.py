# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Contact : shangyameng
# @Name    : __init__.py.py
# @Desc    :


from application.initialization.resource_process import Api
from application.initialization.error_process import register_blueprint_error
from application.initialization.request_process import init_bp_hook_function
from application.initialization.application import logger

from pathlib import Path
from application.config.server_conf import current_config

import os
import re

import importlib


class RegisterBlueprint(object):

    def __init__(self, app):
        self.all_modules = []
        self._app = app
        self.api_ = Api(app)

    def init_register_blueprint(self):
        self.load_all_resource_and_blueprint()
        for current_bp in self.all_modules:
            bp = current_bp.blueprint()
            if current_bp.enable:
                # bp_api_ = Api(bp)
                current_bp.init_resource(Api(bp))
                self._app.register_blueprint(bp, url_prefix=f"{bp.url_prefix}")
                bp_static_dir = f"{current_config.STATIC_FOLDER}/{bp.name}"
                if not Path(bp_static_dir).exists():
                    os.makedirs(bp_static_dir, exist_ok=True)

            # 注册错误
            register_blueprint_error(bp)
            init_bp_hook_function(bp)

    def load_all_resource_and_blueprint(self):
        """
        加载当前文件夹下所有的路由和蓝本
        """
        default_dirs = os.path.dirname(__file__)
        a = ""
        for _dir in [_dir for _dir in os.listdir(default_dirs) if not re.search(r"^[_\.]", _dir)]:
            abs_file_path = f"application/apis/{_dir}"
            module = importlib.import_module(abs_file_path.replace("/", "."))
            importlib.reload(module)
            try:
                current_bp = getattr(module, 'CustomBlueprint')
                self.all_modules.append(current_bp)
            except Exception as e:
                logger.exception(e)
