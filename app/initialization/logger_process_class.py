# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:38 下午
# @Name    : logger_process.py
# @Desc    :

import logging

from logging import config
from pathlib import Path

from flask_log_request_id import RequestIDLogFilter
from config.server_conf import current_config


class Logging(object):
    def __init__(self, log_file_dir=None):
        """
        need pip install Flask-Log-Request-ID、concurrent-log-handler
        :param log_file_dir:
        """
        self.log_file_dir = log_file_dir or current_config.LOG_DIR
        self.log_config = {}
        self.loggers = []

        self._set_default_log_conf()
        self._get_all_loggers()

    #
    # @staticmethod
    # def get_logger(logger_name):
    #     return logging.getLogger(logger_name)

    def add_handler(self,
                    handler_name="default",
                    log_file_path='debug.log',
                    logger_level="debug",
                    formatter="standard",
                    backup_count=5,
                    filters=None,
                    save_file=True,
                    console=True,
                    use_concurrent_log_handler=True,
                    max_bytes=1024 * 1024 * 20,
                    when="d",
                    ):
        filters, level = self._add_handler_set_default_params(filters, logger_level)
        use_handlers = []
        base_handler_conf = {
            'level': level,
            'formatter': formatter,
            'encoding': 'utf-8',
            'filters': filters,  # 使用哪种formatters日志格式
            'filename': log_file_path,  # 日志输出文件位置
            'backupCount': backup_count,  # 备份份数
        }
        if save_file:
            if use_concurrent_log_handler:
                base_handler_conf.update({
                    # 文件格式的日志
                    'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
                    'maxBytes': max_bytes,  # 文件大小
                })
            else:
                base_handler_conf.update({
                    # 日期格式的日志
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "when": when,
                })

            self.log_config["handlers"].update({handler_name: base_handler_conf})
            use_handlers.append(handler_name)
        if console:
            use_handlers.append("console")
        self.log_config["loggers"].update({
            handler_name: {
                "level": logger_level.upper(),
                "handlers": use_handlers,
                "propagate": 0,
                "qualname": handler_name
            },
        })
        self._load_config()

    def _add_handler_set_default_params(self, filters, logger_level):
        if logger_level == "info":
            level = logging.INFO
        elif logger_level == "warning":
            level = logging.WARNING
        elif logger_level == "error":
            level = logging.ERROR
        elif logger_level == "critical":
            level = logging.CRITICAL
        else:
            level = logging.DEBUG
        if filters not in self.log_config["filters"].keys():
            filters = ['req_id_filter']
        return filters, level

    def _set_default_log_conf(self):
        root_log_file = self.log_file_dir + '/root.log'
        ERROR_LOG = self.log_file_dir + '/error.log'
        Path(self.log_file_dir).mkdir(exist_ok=True)

        self.log_config = {
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
                    '()': RequestIDLogFilter  # 获取请求中的 request_id
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': logging.INFO,
                    'formatter': 'standard',
                    'filters': ['req_id_filter']
                },
                'error': {

                    # 文件格式的日志
                    'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
                    'filename': root_log_file,  # 日志输出文件位置
                    'backupCount': 5,  # 备份份数
                    'maxBytes': 1024 * 1024 * 20,  # 文件大小
                    'level': logging.ERROR,
                    'formatter': 'standard',
                    'encoding': 'utf-8',
                    'filters': ['req_id_filter'],  # 使用哪种formatters日志格式
                },
                'info': {

                    # 文件格式的日志
                    'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
                    'filename': root_log_file,  # 日志输出文件位置
                    'backupCount': 5,  # 备份份数
                    'maxBytes': 1024 * 1024 * 20,  # 文件大小
                    'level': logging.INFO,
                    'formatter': 'standard',
                    'encoding': 'utf-8',
                    'filters': ['req_id_filter'],  # 使用哪种formatters日志格式
                },
                'debug': {

                    # 文件格式的日志
                    'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
                    'filename': root_log_file,  # 日志输出文件位置
                    'backupCount': 5,  # 备份份数
                    'maxBytes': 1024 * 1024 * 20,  # 文件大小
                    'level': logging.DEBUG,
                    'formatter': 'standard',
                    'encoding': 'utf-8',
                    'filters': ['req_id_filter'],  # 使用哪种formatters日志格式
                },
            },
            'loggers': {
                "product": {
                    "level": "INFO",
                    "handlers": ["info"],
                    "propagate": 0,
                    "qualname": "product"
                },
                "test": {
                    "level": "DEBUG",
                    "handlers": ["debug"],
                    "propagate": 0,
                    "qualname": "test"
                },
                "console": {
                    "level": "INFO",
                    "handlers": ["console"],
                    "propagate": 0,
                    "qualname": "celery"
                }
            },
            'root': {
                'level': "INFO",
                "propagate": 0,
                'handlers': ['console']
            },
        }
        self._load_config()

    def _get_all_loggers(self):
        self.loggers = list(self.log_config["loggers"].keys())

    def _load_config(self):
        config.dictConfig(self.log_config)

    @classmethod
    def get_logger(cls, logger_name,
                   log_file_path='debug.log',
                   logger_level="debug",
                   formatter="standard",
                   filters=None,
                   backup_count=5,
                   max_bytes=1024 * 1024 * 20,
                   save_file=True,
                   console=True,
                   use_concurrent_log_handler=True,
                   when="d",):

        kwargs = {
            "log_file_path": log_file_path,
            "logger_level": logger_level,
            "formatter": formatter,
            "filters": filters,
            "backup_count": backup_count,
            "max_bytes": max_bytes,
            "save_file": save_file,
            "console": console,
            "use_concurrent_log_handler": use_concurrent_log_handler,
            "when": when
        }
        if logger_name not in Logging().loggers:
            Logging().add_handler(handler_name=logger_name, **kwargs)
        return logging.getLogger(logger_name)


# def get_logger(logger_name,
#                log_file_path='debug.log',
#                logger_level="debug",
#                formatter="standard",
#                filters=None,
#                backup_count=5,
#                max_bytes=1024 * 1024 * 20,
#                save_file=True,
#                console=True,
#                use_concurrent_log_handler=True,
#                when="d",):
#     logger_item = Logging()
#     kwargs = {
#         "log_file_path": log_file_path,
#         "logger_level": logger_level,
#         "formatter": formatter,
#         "filters": filters,
#         "backup_count": backup_count,
#         "max_bytes": max_bytes,
#         "save_file": save_file,
#         "console": console,
#         "use_concurrent_log_handler": use_concurrent_log_handler,
#         "when": when
#     }
#     if logger_name not in logger_item.loggers:
#         logger_item.add_handler(handler_name=logger_name, **kwargs)
#     return logging.getLogger(logger_name)

logger = Logging.get_logger(current_config.LOG_LEVEL)

__all__ = ['logger']
#
# if __name__ == '__main__':
#     logger = get_logger("consoles")
#     logger.info("test")
#     logger.debug("debug")
