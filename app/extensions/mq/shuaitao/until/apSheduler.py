#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 16:49
# @Author  : cst
# @FileName: apSheduler.py
# @Software: PyCharm
# @Describe:
"""此文件可以根据具体业务复杂化选择写或者直接调用原apscheduler接口"""
from apscheduler.triggers.combining import AndTrigger
from flask import current_app


# from .extensions import scheduler  直接导入单例对象操作也行

class APScheduler(object):
    """调度器控制方法"""

    def add_job(self, jobid, func, args, **kwargs):
        """
        添加任务
        :param args:  元祖 -> （1，2）
        :param jobstore:  存储位置
        :param trigger:
                        data ->  run_date   datetime表达式
                        cron ->  second/minute/day_of_week
                        interval ->  seconds 延迟时间
                        next_run_time ->  datetime.datetime.now() + datetime.timedelta(seconds=12))
        :return:
        """
        job_def = dict(kwargs)
        job_def['id'] = jobid
        job_def['func'] = func
        job_def['args'] = args
        job_def = self.fix_job_def(job_def)
        try:
            self.remove_job(jobid)  # 删除原job
        except Exception as e:
            print("无重复id的定时任务")
        return current_app.apscheduler.scheduler.add_job(**job_def)

    def remove_job(self, jobid, jobstore=None):
        """删除任务"""
        current_app.apscheduler.remove_job(jobid, jobstore=jobstore)

    def remove_all_jobs(self, jobstore=None):
        """删除所有任务"""
        current_app.apscheduler.remove_all_jobs(jobstore=jobstore)

    def resume_job(self, jobid, jobstore=None):
        """恢复任务"""
        current_app.apscheduler.resume_job(jobid, jobstore=jobstore)

    def pause_job(self, jobid, jobstore=None):
        """暂停任务"""
        current_app.apscheduler.pause_job(jobid, jobstore=jobstore)

    def shut_down(self, wait=True):
        """
        关闭所有任务
        :param wait:
        :return:
        """
        current_app.apscheduler.shutdown(wait)

    def get_job(self, jobid, jobstore=None):
        """
        获取job信息
        :param jobid:
        :param jobstore:
        :return:
        """
        return current_app.apscheduler.get_job(jobid, jobstore=jobstore)

    def get_jobs(self, jobstore=None):
        """
        获取job信息
        :param jobid:
        :param jobstore:
        :return:
        """
        return current_app.apscheduler.get_jobs(jobstore=jobstore)

    def fix_job_def(self, job_def):
        """维修job工程"""
        if job_def.get('trigger') == 'date':
            job_def['run_date'] = job_def.get('run_date') or None
        elif job_def.get('trigger') == 'cron':
            job_def['hour'] = job_def.get('hour') or "*"
            job_def['minute'] = job_def.get('minute') or "*"
            job_def['week'] = job_def.get('week') or "*"
            job_def['day'] = job_def.get('day') or "*"
            job_def['month'] = job_def.get('month') or "*"
            job_def['year'] = job_def.get('year') or "*"
        elif job_def.get('trigger') == 'interval':
            job_def['seconds'] = int(job_def.get('seconds')) or "*"
        else:
            if job_def.get("andTri"):
                job_def['trigger'] = AndTrigger([job_def.pop("andTri", None), ])
            # job_def['next_run_time'] = job_def.get('next_run_time') or None
        return job_def
