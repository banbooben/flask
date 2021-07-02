#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/9 18:22
# @Author  : shangyameng
# @Email   : shangyameng@datagrand.com
# @Site    :
# @File    : rabbit_factory.py
# @desc    :


class ConnectionFactory(object):

    def create(self, conf, rabbit_class, logger_item):
        rabbit_item = rabbit_class(conf, logger_item)
        return rabbit_item

    def set_host(self):
        ...
