#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:38 下午
# @Author  : shangyameng
# @Email   : 
# @Site    : 
# @File    : ap_scheduler.py
# @desc    :

from flask import request

from initialization.base_resource_process import BaseResource
from initialization.base_error_process import APIException

from APScheduler.ap_scheduler import scheduler

from servers.apscheduler_servers import APSchedulerServers


class APSchedulerResource(BaseResource):
    ap_scheduler_servers_ = APSchedulerServers()

    def get(self):
        data = [{"job_id": job.id, "job_name": job.name} for job in self.ap_scheduler_servers_.get_jobs(scheduler)]
        return self.response(data=data)

    def post(self):

        job_info = self.ap_scheduler_servers_.add_job(scheduler, request.params, request.files)

        return self.response(message="job add ok ", data={"job_id": job_info})


class APSchedulerDeleteResource(APSchedulerResource):

    def delete(self, job_id):
        self.ap_scheduler_servers_.remove_job(scheduler, job_id)
        message = f"job_id: {job_id} is done"
        return self.response(message=message)
