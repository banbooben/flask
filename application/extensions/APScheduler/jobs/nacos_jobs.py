#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2022-04-27 14:17:00
# @LastEditTime: 2022-04-28 13:49:29
# @FilePath: /flask/application/extensions/APScheduler/jobs/nacos_jobs.py

import time
import nacos

from application.initialization.logger_process import logger
from application.tools.nacos_tools import NacosClient

nacos_address = "192.168.2.160:8848"
nacos_namespace = "public"
nacos_username = "nacos"
nacos_password = "nacos"

server_name = "flaskr"
server_ip = "192.168.2.100"
server_port = 50000
server_metadata = {"current_env": "test"}
server_group_name = "SARMN"


class NacosJob(object):
    is_register = None
    client_ = None

    def __new__(cls, *args, **kwargs):
        if not cls.is_register:
            if not cls.client_:
                # logger.info("start init nacos client")
                # logger.info(f"{nacos_address = }")
                # logger.info(f"{nacos_namespace = }")
                # logger.info(f"{nacos_username = }")
                # logger.info(f"{nacos_password = }")
                cls.client_ = NacosClient(nacos_address,
                                          namespace=nacos_namespace,
                                          username=nacos_username,
                                          password=nacos_password)
            # logger.info("start register server")
            # logger.info(f"{server_name = }")
            # logger.info(f"{server_ip = }")
            # logger.info(f"{server_port = }")
            # logger.info(f"{server_group_name = }")
            # logger.info(f"{server_metadata = }")
            cls.is_register = cls.client_.add_naming_instance(server_name,
                                                              server_ip,
                                                              server_port,
                                                              group_name=server_group_name,
                                                              metadata=server_metadata)
        return cls.client_

    # # def __init__(self):
    # def __init__(self, server_addresses, endpoint=None, namespace=None, ak=None, sk=None, username=None, password=None):
    #     self.client_ = nacos.NacosClient(server_addresses,
    #                                      endpoint=endpoint,
    #                                      namespace=namespace,
    #                                      ak=ak,
    #                                      sk=sk,
    #                                      username=username,
    #                                      password=password)

    def send_heartbeat(self, *args, **kwargs):
        logger.info(f"{self.is_register = }")
        logger.info(f"{self.client_ = }")
        logger.info(f"{server_name = }")
        logger.info(f"{server_ip = }")
        logger.info(f"{server_port = }")
        res = self.send_heartbeat(*args, **kwargs)
        logger.info(res)


def keep_heart():
    logger.info("keep heart job start!!!")
    nacos_jobs_ = NacosJob(nacos_address, namespace=nacos_namespace, username=nacos_username, password=nacos_password)
    res = nacos_jobs_.send_heartbeat(server_name, server_ip, server_port, group_name=server_group_name)
    logger.info(res)
    logger.info("end keep heart job")


jobs = {
    keep_heart: {
        "trigger": 'cron',
        "second": '*/4',
        "coalesce": True,
    }
}
