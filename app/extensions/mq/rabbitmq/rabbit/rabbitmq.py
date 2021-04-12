#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/22 22:58
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    : 
# @File    : rabbitmq.py
# @desc    :


import pika


class RabbitBase(object):
    def __init__(self, config, logger_item):
        self.current_config = config
        self.logger = logger_item
        self._connection = None
        self._channel = None

        self.v_host = self.current_config.v_host  # 虚拟网络
        self.username = self.current_config.username or ""  # 用户名
        self.password = self.current_config.password or ""  # 密码
        self.host = self.current_config.host or ""  # 主机
        self.port = self.current_config.port or ""  # 端口
        self.ack = self.current_config.ack or True  # 是否开启消息手动确认机制, 默认是自动确认机制
        self.persist = self.current_config.persist or True  # 消息是否持久化
        self.exchange = self.current_config.exchange or ""  # 交换机名称
        self.exchange_type = self.current_config.exchange_type or ""  # 交换机类型

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        # if self._channel and self._channel.close():
        #     self.close()
        # else:
        #     self.logger.info("已关闭！")

    def connection_by_rrl(self):
        url = "scheme://username:password@host:port/virtual_host?key=value&key=value"
        parameters = pika.connection.URLParameters(url)
        try:
            connection = pika.BlockingConnection(parameters=parameters)
            channel = connection.channel()
        except Exception as e:
            self.logger.exception(e)
            connection, channel = None, None
        self._connection, self._channel = connection, channel

    def connect_by_a(self):
        # 连接mq
        if self.username and self.password:
            credentials = pika.PlainCredentials(username=self.username,
                                                password=self.password)
        else:
            credentials = None
        parameters = pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=credentials
        ) if credentials else pika.ConnectionParameters(host=self.host,
                                                        port=self.port)
        try:
            connection = pika.BlockingConnection(parameters=parameters)
            channel = connection.channel()
        except Exception as e:
            self.logger.exception(e)
            connection, channel = None, None

        self._connection, self._channel = connection, channel

    def create_exchange(self, exchange_name, exchange_type):
        """
        注册一个交换机
        Args:
            exchange_name: 交换机名称
            exchange_type: 交换机类型

        Returns:

        """
        self._channel.exchange_declare(exchange=exchange_name,
                                       exchange_type=exchange_type)

    def create_queue(self, queue, durable=True):
        self._channel.queue_declare(queue=queue, durable=durable)

    def connect(self):
        # 设置账号密码
        if self.username and self.password:
            credentials = pika.PlainCredentials(username=self.username,
                                                password=self.password)
        else:
            credentials = None

        # 创
        parameters = pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=credentials
        ) if credentials else pika.ConnectionParameters(host=self.host,
                                                        port=self.port)
        try:
            # 创建阻塞连接
            connection = pika.BlockingConnection(parameters=parameters)
            channel = connection.channel()

        except Exception as e:
            self.logger.exception(e)
            connection, channel = None, None
        self._connection, self._channel = connection, channel

    def close(self):
        self._connection.close()
        """ 关闭信道并断开连接 """

        if self._channel and self._channel.is_open:  # 检测信道是否还存活
            self._channel.close()  # 关闭信道

        if self._connection and self._connection.is_open:  # 检测连接是否还存活
            self._connection.close()  # 断开连接


class RabbitPublisher(RabbitBase):
    """
    生产者
    """

    def push(self, queue_name: str, message=''):
        # 创建通道
        self.connect()
        if self.exchange and self.exchange_type and self._connection and self._channel:
            self.create_exchange(self.exchange, self.exchange_type)
        self._channel.queue_declare(queue=queue_name)
        # self._channel.basic_qos(prefetch_count=1)

        # delivery_mode为2时表示消息持久化, 其他值时非持久化
        properties = pika.BasicProperties(
            delivery_mode=(2 if self.persist else 0))

        # 开启消息送达确认(注意这里是送达消息队列即可)
        self._channel.confirm_delivery()
        self._channel.basic_publish(exchange=self.exchange,
                                    routing_key=queue_name,
                                    body=message,
                                    properties=properties)
        # 关闭
        self.close()


class RabbitConsumer(RabbitBase):
    """
    消费者
    """

    def get(self, queue_name, func=None):
        # 创建通道
        self.connect()
        if not func:
            func = self.callback

        # 获取任务
        self._channel.basic_consume(on_message_callback=func,
                                    routing_key=queue_name,
                                    auto_ack=True)

        self._channel.start_consuming()
        # 关闭
        self.close()

    def callback(self):
        self.logger.info("start compare the message")
