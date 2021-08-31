#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2021-08-30 14:25:06
# @LastEditTime: 2021-08-31 13:58:02
# @FilePath: /app/APScheduler/jobs/clear_expired_files_jobs.py
import os

from tools.file_tools import FileTools
from initialization.application import logger


class ClearExpiredFileJobs(object):
    def __init__(self, *args, **kwargs):
        self.file_tools_ = FileTools()
        self._delete_time = 10
        self._dirs_68 = []

    def get_need_del_files(self, dir_path):
        need_del_files = []
        all_files = self.file_tools_.load_all_files(dir_path)
        for file_path in all_files:
            c_time = os.path.getctime(file_path)
            print(c_time)
        # logger.info(all_files)


if __name__ == '__main__':
    dir_path = "."
    a = ClearExpiredFileJobs()
    a.get_need_del_files(dir_path)





