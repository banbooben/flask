#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/16 16:52
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    :
# @File    : extract_business_layer.py
# @desc    :

from celery_task.celery_process import celery_app
from tools.logger_process_class import Logging

# from business_layer import extract_business

logger = Logging.get_logger(__name__)


@celery_app.task()
def document_parse(params):
    logger.info(params)
    return params
