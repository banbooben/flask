"""
Created on 2019年1月14日
@author: ljbai

comment by LuShuYang:
    Flask的log分为两个部分, 一个是在业务代码里面使用的app.logger, 一个是werkzueg的logger,

    在本地的时候我们将werkzueg的logger和app.logger重定向到标注输出中,

    如果在部署的时候, 使用gunicorn部署, 再将gunicorn的logger和app的logger都重定向到File中.

    因此不修改werkzeug的logger, 且不要使用werkzueg进行部署.
"""
import logging
from logging import config
import os

# from configs.base import PROJECT_NAME
# from configs.sysconf import LOG_LEVEL
from config.server_conf import current_environment, current_config

LOG_FILE_PATH = os.path.join(current_config.LOG_DIR, "root.log")
LOG_LEVEL = current_config.LOG_LEVEL

logger = logging.getLogger(current_config.PROJECT_NAME)  # same as app.logger
logger.setLevel(LOG_LEVEL)

formatter = logging.Formatter('%(asctime)s - %(request_id)s - %(levelname)s - %(filename)s:%(lineno)s'
                              ' - [%(funcName)s]:  %(message)s')


class RequestIdLogRecord(logging.LogRecord):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from flask import request
        try:
            self.request_id = request.request_id
        except:
            self.request_id = "null"


logging.setLogRecordFactory(RequestIdLogRecord)

# # 日志输出到文件
# logger.handlers.append(logging.FileHandler(LOG_FILE_PATH, encoding='UTF-8'))

# 日志输出到终端
logger.handlers.append(logging.StreamHandler())

for handler in logger.handlers:
    handler.setFormatter(formatter)
    # handler.formatter = formatter
    # logger.addHandler(handler)

if __name__ == '__main__':
    ...
