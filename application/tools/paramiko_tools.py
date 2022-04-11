import paramiko
from setuptools import unicode_utils
import logging

logger = logging.getLogger('log')


class SSHConnection(object):
    def __init__(self, host_dict):
        self.host = host_dict['host']
        self.port = host_dict['port']
        self.username = host_dict['username']
        self.pwd = host_dict['pwd']
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host ,self.port))
        transport.connect(username=self.username ,password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def run_cmd(self, command):
        """
         执行shell命令,返回字典
         return {'color': 'red','res':error}或
         return {'color': 'green', 'res':res}
        :param command:
        :return:
        """
        logger.info("run command: %s" % command)
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        for i in range(3):
            try:
                stdin, stdout, stderr = ssh.exec_command(command)
            except Exception as ex:
                print("exec_command:%s err:%s" % (command, str(ex)))
            else:
                break
        # 获取命令结果
        res = to_str(stdout.read())
        # res = unicode_utils.to_str(stdout.read())
        # 获取错误信息
        error = to_str(stderr.read())
        # error = unicode_utils.to_str(stderr.read())
        # 如果有错误信息，返回error
        # 否则返回res
        # print("res+++++++++++++++++++",res)
        # print("error+++++++++++++++++++",error)
        if error.strip():
            return {'color':'red' ,'res' :error}
        else:
            return {'color': 'green', 'res' :res}

    def upload(self, local_path, target_path):
        # 连接，上传
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 上传至服务器 /tmp/test.py
        for i in range(3):
            try:
                sftp.put(local_path, target_path, confirm=True)
                # 增加权限
                # sftp.chmod(target_path, os.stat(local_path).st_mode)
                sftp.chmod(target_path, 0o644)  # 注意这里的权限是八进制的，八进制需要使用0o作为前缀
            except Exception as ex:
                raise ex
                logger.error("put:%s to %s err:%s" % (local_path,target_path, str(ex)))
            else:
                break
        # print(os.stat(local_path).st_mode)



    def download(self ,target_path, local_path):
        # 连接，下载
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 下载至服务器 /tmp/test.py
        sftp.get(target_path, local_path)

    # 销毁
    def __del__(self):
        self.close()


def to_str(bytes_or_str):
    """
    把byte类型转换为str
    :param bytes_or_str:
    :return:
    """
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value