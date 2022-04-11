#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:36 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : __init__.py.py
# @desc    :

from application.initialization.blueprint_process import CustomBlueprintBase, Blueprint, Api
from application.config.server_conf import current_config

scheduler_bp = Blueprint("scheduler",
                         __name__,
                         static_folder=f'{current_config.STATIC_FOLDER}/scheduler',
                         static_url_path='/',
                         url_prefix="/scheduler")


class CustomBlueprint(CustomBlueprintBase):
    _enable = True
    _current_bp = scheduler_bp

    @classmethod
    def init_resource(cls, api_: Api):

        from .ap_scheduler import (
            APSchedulerJobsBaseResource,
            APSchedulerJobsResource,
            APSchedulerJobResource,
            DeleteAllAPSchedulerJobsResource
        )

        api_.add_resource(APSchedulerJobsBaseResource, "/jobs"),
        api_.add_resource(DeleteAllAPSchedulerJobsResource, "/delete/all"),
        api_.add_resource(APSchedulerJobsResource, "/jobs/<string:job_id>"),
        api_.add_resource(APSchedulerJobResource, "/jobs/<string:job_id>/<string:active>"),

