#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:38 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : ap_scheduler.py
# @desc    :

from flask import request
from flask_restful import Resource

from initialization.application import custom_response_
from initialization.base_error_process import APIException

from APScheduler.ap_scheduler import scheduler

from servers.apscheduler_servers import APSchedulerServers

ap_scheduler_servers_ = APSchedulerServers()


class APSchedulerJobsBaseResource(Resource):
    def get(self):
        data = [{"job_id": job.id, "job_name": job.name} for job in ap_scheduler_servers_.get_jobs(scheduler)]
        return custom_response_.response(data=data)

    def post(self):

        job_info = ap_scheduler_servers_.add_job(scheduler, request.params, request.files)

        return custom_response_.response(message="job add ok ", data={"job_id": job_info})


class APSchedulerJobsResource(Resource):
    def delete(self, job_id):
        ap_scheduler_servers_.remove_job(scheduler, job_id)
        message = f"job_id: {job_id} is done"
        return custom_response_.response(message=message)

    def patch(self, job_id):
        ap_scheduler_servers_.update_job(scheduler, job_id)
        message = f"job_id: {job_id} is done"
        return custom_response_.response(message=message)


class APSchedulerJobResource(Resource):
    def post(self, job_id, active):
        job = ap_scheduler_servers_.jobs_manage(scheduler, job_id, active)
        return job
