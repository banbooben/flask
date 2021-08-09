import os
import uuid

from qam.qam_server import QAMServer
from qam.qam_proxy import QAMProxy, QAMMethodNotFoundException, QAMException


class FunctionsTools(object):

    @staticmethod
    def get_uuid():
        return uuid.uuid4()

    @staticmethod
    def load_file(file_path, **kwargs):
        if not file_path or os.path.exists(file_path):
            return ''
        method = kwargs.get("method", "r")
        with open(file_path, method) as file:
            file_words = file.readlines()
            return file_words


class MyQAMServer(object):

    def __init__(self, hostname="127.0.0.1", port=5672,
                 username="admin", password="admin",
                 server_id="qam_master", vhost="/",
                 serializer='pickle', ):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.server_id = server_id
        self.vhost = vhost
        self.serializer = serializer

    def create(self):
        qam_server = QAMServer(hostname=self.hostname,
                               port=self.port,
                               username=self.username,
                               password=self.password,
                               server_id=self.server_id,
                               vhost=self.vhost,
                               serializer=self.serializer, )
        return qam_server

    def register(self):
        qam_server = self.create()
        function_tools_ = FunctionsTools()
        # qam_server.register_function(function_tools_, "function")
        qam_server.register_class(function_tools_, "function_tools")
        qam_server.serve()


class MyQAMProxy(object):

    def __init__(self, hostname="127.0.0.1", port=5672,
                 username="admin", password="admin",
                 server_id="qam_master", vhost="/",
                 serializer='pickle', client_id="client_id_test"):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.server_id = server_id
        self.client_id = client_id
        self.vhost = vhost
        self.serializer = serializer

    def create(self):
        qam_proxy = QAMProxy(hostname=self.hostname,
                             port=self.port,
                             username=self.username,
                             password=self.password,
                             server_id=self.server_id,
                             vhost=self.vhost,
                             serializer=self.serializer,
                             client_id=self.client_id)
        return qam_proxy


if __name__ == "__main__":
    MyQAMServer().register()

    test = MyQAMProxy().create()

    uuid = test.function_tools_.get_uuid()

    print(uuid)
