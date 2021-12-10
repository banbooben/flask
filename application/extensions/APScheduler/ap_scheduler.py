#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2021-08-18 18:12:30
# @LastEditTime: 2021-10-11 21:37:08
# @FilePath: /bdo/flask_app/APScheduler/test.py

# import sys
from application.initialization.logger_process import logger
from pytz import utc
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

scheduler_config = {
    "jobstores": {
        'default': SQLAlchemyJobStore(url='sqlite:///./jobs.sqlite')
    },
    "executors": {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(4)
    },
    "job_defaults": {
        'coalesce': False,
        'max_instances': 3
    },
    "timezone": utc
}


def listener(event):
    if event.exception:
        ...


scheduler = BackgroundScheduler(**scheduler_config)
scheduler.start()
scheduler.remove_all_jobs()
scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler._logger = logger
