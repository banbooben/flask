#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/9 18:22
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    :
# @File    : rabbit_factory.py
# @desc    :

import pika


class ConnectionFactory(object):
    """
    client与rabbitmq链接时需要设置心跳值，大多数场景下5～20S比较好
    一些网络工具如Haproxy及设备如硬件负载均衡会在这些连接在一定时间段内没有活动时，会关闭空闲的TCP连接。大多数时间这是不可取的。
    当启用心跳时，会带来周期性的轻网络流量。因此，心跳具有保护客户端连接的作用，这些客户端可以在一段时间内空闲，以防止代理或负载均衡设备过早的关闭。
    当心跳超时时间为30s时，产生轻网络流量的周期为15s。5到15s内范围内的活动，可以满足大多数常用代理或负载均衡设备的默认值。


    """
    def __init__(self):
        self._connection = None
        self._channel = None

        self.v_host = "/"  # 虚拟网络
        self._username = "guest"  # 用户名
        self._password = "guest"  # 密码
        self._host = "127.0.0.1"  # 主机
        self._port = "5673"  # 端口
        self._ack = True  # 是否开启消息手动确认机制, 默认是自动确认机制
        self._persist = True  # 消息是否持久化
        self._exchange = ""  # 交换机名称
        self._exchange_type = ""  # 交换机类型

    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password

    def set_host(self, host):
        self._host = host

    def set_port(self, port):
        self._port = port

    def set_ack(self, ack):
        self._ack = ack

    def set_persist(self, persist):
        self._persist = persist

    def set_exchange(self, exchange):
        self._exchange = exchange

    def set_exchange_type(self, exchange_type):
        self._exchange_type = exchange_type

    def create(self, conf, rabbit_class, logger_item):
        rabbit_item = rabbit_class(conf, logger_item)
        return rabbit_item

    def create_connection(self):
        # 连接mq
        if self._username and self._password:
            credentials = pika.PlainCredentials(
                username=self._username,
                password=self._password,
            )
        else:
            credentials = None

        parameters = pika.ConnectionParameters(
            host=self._host,
            port=self._port,
            credentials=credentials,
            heartbeat_interval=10,
            blocked_connection_timeout=300
        ) if credentials else pika.ConnectionParameters(
            host=self._host,
            port=self._port,
            heartbeat_interval=10,
            blocked_connection_timeout=300)
        try:
            connection = pika.BlockingConnection(parameters=parameters)
        except Exception as e:
            # self.logger.exception(e)
            connection = None
        return connection

    def create_channel(self):
        ...
