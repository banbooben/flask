#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:38 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : test.py
# @desc    :

from flask import request

from application.apis.apscheduler import scheduler_bp
from application.extensions.APScheduler.ap_scheduler import scheduler

from application.initialization.resource_process import BaseResource
from application.extensions.APScheduler.apscheduler_servers import APSchedulerServers


class ApSchedulerBaseResource(BaseResource):

    ap_scheduler_servers_ = APSchedulerServers()


class APSchedulerJobsBaseResource(ApSchedulerBaseResource):

    @scheduler_bp.doc(description="获取所有定时任务")
    def get(self):
        data = [{
            "job_id": job.id,
            "job_name": job.name,
        } for job in
            self.ap_scheduler_servers_.get_jobs(scheduler)]
        return self.response(data=data)

    @scheduler_bp.doc(description="上传py脚本文件，添加定时任务")
    def post(self):
        job_info = self.ap_scheduler_servers_.add_job(scheduler, request.params, request.files)

        return self.response(message="job add ok ", data={"job_id": job_info})


class APSchedulerJobsResource(ApSchedulerBaseResource):
    @scheduler_bp.doc(description="根据ID删除定时任务")
    def delete(self, job_id):
        self.ap_scheduler_servers_.remove_job(scheduler, job_id)
        message = f"job_id: {job_id} is done"
        return self.response(message=message)

    @scheduler_bp.doc(description="根据ID暂停")
    def patch(self, job_id):
        self.ap_scheduler_servers_.update_job(scheduler, job_id, **request.params)
        message = f"job_id: {job_id} is done"
        return self.response(message=message)

    @scheduler_bp.doc(description="获取定时任务的详细信息")
    def get(self, job_id):
        job = self.ap_scheduler_servers_.get_job(scheduler, job_id)
        data = {"job_id": job.id,
                "job_name": job.name,
                "func_ref": job.func_ref,
                "next_run_time": job.next_run_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
        return self.response(data=data)


class APSchedulerJobResource(ApSchedulerBaseResource):
    @scheduler_bp.doc(description="")
    def post(self, job_id, active):
        job = self.ap_scheduler_servers_.jobs_manage(scheduler, job_id, active)
        data = {"job_id": job.id,
                "job_name": job.name,
                "func_ref": job.func_ref,
                "next_run_time": job.next_run_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
        message = f"job_id: {job_id}, status: {active}"
        return self.response(data=data, message=message)


class DeleteAllAPSchedulerJobsResource(ApSchedulerBaseResource):

    def delete(self):
        del_job_ids = self.ap_scheduler_servers_.delete_all_job(scheduler)
        return self.response(data={"jobs_id": del_job_ids, "total": len(del_job_ids)})

