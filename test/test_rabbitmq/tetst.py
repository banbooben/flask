import json
import time
import random

from initialization.application import logger
from rabbit_factory import ConnectionFactory
from rabbitmq import RabbitPublisher, RpcRabbitPublisher


def create_and_connect_mq():
    conn = ConnectionFactory()
    # # 普通模式
    # mq_item = conn.create(RabbitPublisher, "admin", "admin", "127.0.0.1", 5672)

    # RPC模式
    mq_item = conn.create(RpcRabbitPublisher, "admin", "admin", "127.0.0.1", 5672)

    mq_item.connect()
    number = 0
    while number < 1:
        # # 工作模式
        # mq_item.push(queue_name="hello", message=str(i))

        # # 发布订阅模式
        # mq_item.push(exchange="logs", exchange_type="fanout", message="Hello world!" + str(number))

        # # 路由模式
        # mq_item.push(exchange="direct_logs", exchange_type="direct", message="info" + str(number),
        #              routing_key="log:info")
        # mq_item.push(exchange="direct_logs", exchange_type="direct", message="error" + str(number),
        #              routing_key="log:error")

        # # topic模式
        # mq_item.push(exchange="com_list", exchange_type="topic", message="升值" + str(number),
        #              routing_key=["data.beijing.shanghai.guangzhou",
        #                           "data.chengdu.suzhou.zhengzhou",
        #                           "data.chengdu"])
        # mq_item.push(exchange="com_list", exchange_type="topic", message="加薪" + str(number),
        #              routing_key=["data.beijing.shanghai.guangzhou",
        #                           "data.chengdu.suzhou.zhengzhou",
        #                           "data.chengdu.lasa"])

        # rpc
        # mq_item.push(queue_name="rpc_queue", message="RPC 调用演示",)
        message = json.dumps({"task": "uuid"})
        res = mq_item.rpc_server(message=message)
        logger.info(f"response {res}")

        number += 1
        time.sleep(random.random())
    # mq_item.close()
    # mq_item.push(exchange="logs", exchange_type="fanout", message=str(i))


if __name__ == "__main__":
    create_and_connect_mq()
