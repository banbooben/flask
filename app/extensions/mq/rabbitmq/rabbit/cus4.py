import json

from rabbit_factory import ConnectionFactory
from rabbitmq import RabbitConsumer, RpcRabbitConsumer
# from local_logger import logger
# import time

import logging
logger = logging.getLogger()

# import pika


# def on_request(ch, method, props, body):
#     response = body.decode()
#     logger.info(f"body {response}")
#
#     ch.basic_publish(exchange='',
#                      routing_key=props.reply_to,
#                      properties=pika.BasicProperties(correlation_id=props.correlation_id),
#                      body=str(response))
#     ch.basic_ack(delivery_tag=method.delivery_tag)


def create_and_connect_mq():
    conn = ConnectionFactory()
    # # 普通模式
    # mq_item = conn.create(RabbitConsumer, "admin", "admin", "127.0.0.1", 5672)

    # RPC模式
    mq_item = conn.create(RpcRabbitConsumer, "admin", "admin", "127.0.0.1", 5672)

    mq_item.connect()
    # # 工作模式
    # mq_item.get(queue_name="log:test:1")

    # # 发布订阅模式
    # mq_item.get(exchange="logs", exchange_type="fanout",  queue_name="log:test:1")

    # # 路由模式
    # mq_item.get(exchange="direct_logs", exchange_type="direct", queue_name="log:info", func=test)

    # # Topic模式
    # mq_item.get(exchange="com_list", exchange_type="topic",
    #             queue_name="lasa", routing_key=["data.#.lasa.#"],
    #             func=test)

    # rpc模式
    # message = json.dumps({"task": "uuid"})
    # mq_item.rpc_server(message=message)
    mq_item.get(queue_name="rpc_queue", func=mq_item.on_request)

    mq_item.close()


if __name__ == "__main__":
    create_and_connect_mq()
