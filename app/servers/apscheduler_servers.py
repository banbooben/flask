#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 4:49 下午
# @Author  : shangyameng
# @Email   :
# @Site    :
# @File    : apscheduler_servers.py
# @desc    :

from initialization.application import logger
from initialization.base_error_process import APIException

from utils.load_function import load_function


class APSchedulerServers(object):
    def add_job(self, scheduler, params, files):
        job_func = params.get('job_func', None)
        if job_func:
            del params["job_func"]
            # obj_name, func_name = job_func.split(".", 1)
            # obj = load_function("APScheduler/jobs", obj_name)
            job_info = self._add_job(scheduler, eval(job_func), **params)
        else:
            raise APIException("hob_func error")
        return job_info

    def update_job(self, schedule, job_id, params):
        return schedule.reschedule_job(job_id, **params)

    def jobs_manage(self, job_id, active):
        if active == "pause":
            job = self.pause_job(job_id, active)
        elif active == "resume":
            job = self.resume_job(job_id, active)
        elif active == "run":
            job = self.run_job(job_id, active)
        else:
            APIException("error ")
        return job

    def get_jobs(self, schedule):
        return schedule.get_jobs()

    def get_job(self, schedule, job_id):
        return schedule.get_job(job_id)

    def remove_job(self, schedule, job_id):
        return schedule.remove_job(job_id)

    def _add_job(self, scheduler, job, **kwargs):
        job_obj = scheduler.add_job(job, **kwargs)
        logger.info("job add ok")
        return {"job_id": job_obj.id, "job_name": job_obj.name}

    def pause_job(self, schedule, job_id):
        return schedule.pause_job(job_id)

    def resume_job(self, schedule, job_id):
        return schedule.resume_job(job_id)

    def run_job(self, schedule, job_id):
        return schedule.run_job(job_id)
