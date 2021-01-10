# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:38 下午
# @Name    : logger_process.py
# @Desc    :

import logging

from logging import config

from flask_log_request_id import RequestIDLogFilter
from config.server_conf import current_config

ROOT_LOG = str(current_config.LOG_DIR / 'root.log')
ERROR_LOG = str(current_config.LOG_DIR / 'error.log')

LOG_CONF = {
    'version': 1,
    'incremental': False,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': ('%(asctime)s - %(request_id)s - %(levelname)s - %(filename)s:%(lineno)s'
                       ' - [%(funcName)s]:  %(message)s'),
        }
    },
    'filters': {
        'req_id_filter': {
            '()': RequestIDLogFilter
        }
    },
    'handlers': {
        'default': {
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'level': logging.ERROR,
            'formatter': 'standard',
            'filename': ROOT_LOG,  # 日志输出文件位置
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'encoding': 'utf-8',
            'filters': ['req_id_filter'],  # 使用哪种formatters日志格式
        },
        'error': {
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'level': logging.ERROR,
            'formatter': 'standard',
            'filename': ERROR_LOG,
            'maxBytes': 1024 * 1024 * 20,  # 单个日志文件最大 20M
            'backupCount': 5,
            'encoding': 'utf-8',
            'filters': ['req_id_filter']
        },
        'info': {
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'level': logging.INFO,
            'formatter': 'standard',
            'filename': ROOT_LOG,
            'maxBytes': 1024 * 1024 * 20,
            'backupCount': 5,
            'encoding': 'utf-8',
            'filters': ['req_id_filter']
        },
        'debug': {
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'level': logging.DEBUG,
            'formatter': 'standard',
            'filename': ROOT_LOG,
            'maxBytes': 1024 * 1024 * 20,
            'backupCount': 5,
            'encoding': 'utf-8',
            'filters': ['req_id_filter']
        },
        'stream_info': {
            'class': 'logging.StreamHandler',
            'level': logging.INFO,
            'formatter': 'standard',
            'filters': ['req_id_filter']
        }
    },
    'loggers': {
        'default': {
            'level': logging.DEBUG,
            'propagate': False,
            # 'handlers': ['stream_info']
            'handlers': ['stream_info', 'info', 'error']
        },
        "product": {
            "level": "DEBUG",
            "handlers": ["debug"],
            "propagate": 1,
            "qualname": "product"
        },
        "test": {
            "level": "INFO",
            "handlers": ["info"],
            "propagate": 0,
            "qualname": "test"
        }
    },
    'root': {
        'level': logging.DEBUG,
        'handlers': ['stream_info', 'info']
    },
}

config.dictConfig(LOG_CONF)
logger = logging.getLogger(current_config.LOG_LEVEL)

__all__ = ['logger']
