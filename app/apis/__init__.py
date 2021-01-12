# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:47 下午
# @Contact : shangyameng@datagrand.com
# @Name    : __init__.py.py
# @Desc    :


from flask_restful import Api

from .user import user
from initialization.error_process import register_blueprint_error

all_api = (
    user,
)


def register_resource_and_blueprint(app):
    api = Api(app)

    for api_obj in all_api:

        for blueprint_api in api_obj.get("DEFAULT_RESOURCE", ()):
            for resource, url in blueprint_api:
                api.add_resource(resource, url)

        for bp in api_obj.get("ALL_BLUEPRINT", ()):
            app.register_blueprint(bp, url_prefix="/{}".format(bp.name))
            register_blueprint_error(bp)
