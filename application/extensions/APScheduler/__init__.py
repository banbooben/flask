#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2021-08-18 18:12:30
# @LastEditTime: 2021-08-18 18:45:45
# @FilePath: /APScheduler/APScheduler/__init__.py


def schedule_init():
    from .ap_scheduler import scheduler
    from .jobs import all_jobs

    current_jobs = {}
    _ = [current_jobs.update(item) for item in all_jobs]

    for job, kwargs in current_jobs.items():
        scheduler.add_job(job, **kwargs)
