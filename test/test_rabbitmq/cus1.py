from rabbit_factory import ConnectionFactory
from rabbitmq import RabbitConsumer
from initialization.application import logger
import time


def test(channel, method, properties, body: bytes):
    logger.info(f"start :  {body.decode()}")

    channel.basic_ack(delivery_tag=method.delivery_tag)


def create_and_connect_mq():
    conn = ConnectionFactory()
    mq_item = conn.create(RabbitConsumer, "admin", "admin", "127.0.0.1", 5672)

    mq_item.connect()

    # # 工作模式
    # mq_item.get(queue_name="log:test:1")

    # # 发布订阅模式
    # mq_item.get(exchange="logs", exchange_type="fanout",  queue_name="log:test:1")

    # # 路由模式
    # mq_item.get(exchange="direct_logs", exchange_type="direct",
    #             queue_name="log:info", routing_key="log:info",
    #             func=test)

    # Topic模式
    mq_item.get(exchange="com_list", exchange_type="topic",
                queue_name="all_data", routing_key="data.#",
                func=test)

    # 关闭
    mq_item.close()


if __name__ == "__main__":
    create_and_connect_mq()
