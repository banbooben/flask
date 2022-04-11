#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:36 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : __init__.py.py
# @desc    :

# from .blueprint import scheduler

# from flask import Blueprint
from typing import Tuple

from application.initialization.blueprint_process import CustomBlueprintBase, Blueprint, Api
from application.config.server_conf import current_config

auth = Blueprint("auth",
                 __name__,
                 static_folder=f'{current_config.STATIC_FOLDER}/auth',
                 static_url_path='/',
                 url_prefix="/auth")


class CustomBlueprint(CustomBlueprintBase):
    _enable = True
    _current_bp = auth

    @classmethod
    def init_resource(cls, api_: Api):

        from .test import (
            AuthTest,
        )

        api_.add_resource(AuthTest, "/")
