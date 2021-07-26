from rabbit_factory import ConnectionFactory
from rabbitmq import RabbitConsumer
from local_logger import logger
import time


def create_and_connect_mq():
    conn = ConnectionFactory()
    mq_item = conn.create(RabbitConsumer, "admin", "admin", "127.0.0.1", 5672)

    # mq_item.connect()
    i = 0
    while i < 100:
        mq_item.get("hello")
        logger.info(i)
    mq_item.close()


if __name__ == "__main__":
    create_and_connect_mq()
