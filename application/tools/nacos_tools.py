#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2022-04-27 12:47:34
# @LastEditTime: 2022-04-28 13:19:22
# @FilePath: /flask/application/tools/nacos_tools.py

import nacos
# from application.initialization.application import logger
from loguru import logger


class NacosClient(nacos.NacosClient):
    _client = None

    def __new__(cls, *args, **kwargs):
        if not cls._client:
            logger.info(f"{args = }")
            logger.info(f"{kwargs = }")
            cls._client = nacos.NacosClient(*args, **kwargs)
        return cls._client

    def __init__(self, server_addresses, endpoint=None, namespace=None, ak=None, sk=None, username=None, password=None):
        logger.info("start init nacos client")
        logger.info(f"{server_addresses = }")
        logger.info(f"{namespace = }")
        logger.info(f"{username = }")
        logger.info(f"{password = }")
        super().__init__(server_addresses, endpoint, namespace, ak, sk, username, password)

    def add_naming_instance(self,
                            service_name,
                            ip,
                            port,
                            cluster_name=None,
                            weight=1,
                            metadata=None,
                            enable=True,
                            healthy=True,
                            ephemeral=True,
                            group_name=...):
        if not self.is_register:
            logger.info("start register server")
            logger.info(f"{service_name = }")
            logger.info(f"{ip = }")
            logger.info(f"{port = }")
            logger.info(f"{group_name = }")
            logger.info(f"{metadata = }")
            return super().add_naming_instance(service_name, ip, port, cluster_name, weight, metadata, enable, healthy,
                                               ephemeral, group_name)
        else:
            return True

    # def send_heartbeat(self, *args, **kwargs):
    #     res = self.send_heartbeat(*args, **kwargs)
    #     logger.info(res)

    # def send_heartbeat(self,
    #                    service_name,
    #                    ip,
    #                    port,
    #                    cluster_name=None,
    #                    weight=1,
    #                    metadata=None,
    #                    ephemeral=True,
    #                    group_name=...):
    #     return super().send_heartbeat(service_name, ip, port, cluster_name, weight, metadata, ephemeral, group_name)


# # class NacosTools(object):
# class NacosTools(object):

#     def __init__(self) -> None:
#         self._client = NacosClient(nacos_address,
#                                    namespace=nacos_namespace,
#                                    username=nacos_username,
#                                    password=nacos_password)

if __name__ == "__main__":

    nacos_address = "192.168.2.160:8848"
    nacos_namespace = "public"
    nacos_username = "nacos"
    nacos_password = "nacos"

    server_name = "flaskr"
    server_ip = "192.168.2.100"
    server_port = 50000
    server_metadata = {"current_env": "test"}
    server_group_name = "SARMN"
    nacos_tools_ = NacosClient(nacos_address, nacos_namespace)
    nacos_tools_.add_naming_instance(server_name,
                                     server_ip,
                                     server_port,
                                     group_name=server_group_name,
                                     metadata=server_metadata)
