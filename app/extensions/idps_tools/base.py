#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/21 12:04
# @Author  : shangyameng@datagrand.com
# @Site    :
# @File    : base.py

# from conf.api_config import *

from functools import wraps
from initialization.application import logger
from config.server_conf import current_config

import requests
import json
import pymysql
import os
# from conf import config


class IdpsApiBase(object):
    access_token = ""
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    }

    def __init__(self, config, product=True, jumper_username="shangyameng"):
        self.config = config
        self.re_try = self.config.re_try
        self.username = self.config.username
        self.password = self.config.password
        self.host = self.config.host
        self.port = self.config.port
        self.logger = logger

        self.logon_route = self.config.logon_route
        self.logon_url = "http://{}/{}".format(self.host, self.logon_route)

        self.creat_request_route = self.config.creat_request_route
        self.create_request_url = "http://{}/{}".format(self.host, self.creat_request_route)

        self.feature_type_id = self.config.test_id
        self.get_extract_result_route = self.config.get_extract_result_route
        self.get_table_result_url = "http://{}/{}".format(self.host, self.get_extract_result_route)

        self.tag_types_route = self.config.tag_types_route
        self.tag_types_key = self.config.tag_types_key
        self.tag_types_url = "http://{}/{}".format(self.host, self.tag_types_route)

        self.bizlicense = "http://ysocr.datagrand.cn/ysocr/bizlicense_extract"

        self.all_tags = self._get_all_filed_id_and_name()

        self.db_host = self.config.db_host
        self.db_port = self.config.db_port
        self.db_user = self.config.db_user
        self.db_password = self.config.db_password
        self.db_database = self.config.db_database
        self.charset = self.config.charset
        self.download_file_url = f"http://{self.host}/upload/"
        self.connection, self.cursor = None, None

        self.product = self.config.product
        self.jumper_username = jumper_username

        if not os.path.exists(self.config.upload):
            os.makedirs(self.config.upload)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_trace):
        if self.cursor:
            self.cursor.close()
            self.logger.info("已关闭数据库连接！")
        else:
            self.logger.info("已关闭")

    def _connect_jumper_server(self):
        if self.product:
            ip = "172.17.132.132"
        else:
            ip = "172.17.132.130"
        cmd = f"""ssh -f -p 58422 {self.jumper_username}@jumper-huabei2-vpc.datagrand.com -L {
        self.db_port}:{ip}:{self.db_port} -N"""
        status = os.system(cmd)
        if status != 0:
            return False
        return True

    # @staticmethod
    def _login_by_user(self):
        """
        登录系统
        Returns:

        """
        if self.logon_url:
            data = {"username": self.username, "password": self.password}
            request_result = requests.post(url=self.logon_url, data=data, headers=self.headers)
            if request_result.status_code == 200:
                result = json.loads(request_result.text)
                if result:
                    self.access_token = "Bearer " + result.get("access_token", None)
                    self.headers.update({"Authorization": self.access_token})
                    return "登录成功"
            return "登录失败"
        return "缺少登录地址"

    def _get_all_filed_id_and_name(self):
        self._login_by_user()
        all_doctype = self._get_all_tag_types()
        all_doctype = all_doctype.get("items") if all_doctype else None
        all_tags = {}
        if all_doctype:
            for item in all_doctype:
                item_tags = {}
                doctype = item["id"]
                if item["tags"]:
                    [item_tags.update({str(field["id"]): field["name"]}) for field in item["tags"]]
                all_tags.update({doctype: item_tags}) if item_tags else None
        return all_tags

    def _get_all_tag_types(self):
        """
        获取所有的文档类型信息
        Returns:
            所有文档类型信息，ID、name、tags等
        """
        self._login_by_user()
        url = self.tag_types_url + self.tag_types_key
        result = self._requests_processor(url)
        return json.loads(result.content.decode("utf-8")) if result else None

    def _requests_processor(self, url, method="GET", params=None, file=None):
        if not self.access_token:
            self._login_by_user()
        if method == "GET":
            send_review_request = requests.get(url, headers=self.headers)
        else:
            send_review_request = {
                'PUT': requests.put,
                'POST': requests.post,
                'DELETE': requests.delete,
            }[method](url, headers=self.headers, data=params, files=file)
        if send_review_request.status_code == 401:
            self._login_by_user()
            if self.re_try > 0:
                self.re_try -= 1
                return self._requests_processor(url=url, method=method, params=params, file=file)
            else:
                return {}
        else:
            result = send_review_request if send_review_request else None
            self.re_try = self.config.re_try
            return result

    def _connect_and_get_cursor(self):
        """
        创建连接并初始化游标
        :return:
        """
        connection = pymysql.connect(host=self.db_host,
                                     port=self.db_port,
                                     user=self.db_user,
                                     password=self.db_password,
                                     db=self.db_database,
                                     charset=self.charset)
        cursor = connection.cursor()
        self.connection, self.cursor = connection, cursor

    def _execute_by_select(self, sql: str):
        """
        执行sql语句并返回执行结果
        :param sql:
        :return:
        """
        try:

            res = []
            if self.cursor and sql:
                self.cursor.execute(sql)
                res = self.cursor.fetchall()
                return res
            return res
        except Exception as e:
            self.logger.info(e)
            return []
        finally:
            self.cursor.close()

    def _save_file(self, file_text, file_name: str, json_save_path: str, file_type: str):
        if file_text and json_save_path and os.path.exists(json_save_path):
            self.logger.info(f"start download {file_name}")

            if file_type == "pdf":
                write_type = "wb"
            else:
                write_type = "w"
                file_text = file_text.decode("utf-8")
            try:
                with open(os.path.join(json_save_path, file_name), write_type) as f:
                    f.write(file_text)
                    self.logger.info(f"{os.path.join(json_save_path, file_name)} is downloaded")
            except Exception as e:
                self.logger.info(e)

    def _select_files_uuid_by_id(self, ids: tuple, id_type="task_id", no_single=True):
        """

        Args:
            ids: 需要查询的任务ID
            id_type: 传入的ID类型，默认是taskID
            no_single: 是否不是单文件下载

        Returns:
            ((unique_name, doctype, doc_type), )
        """
        if ids:
            self._connect_jumper_server()
            self._connect_and_get_cursor()
        else:
            return None
        ids = repr(ids).replace(",)", ")")
        sql1 = f"SELECT a.unique_name, b.tag_type_id, a.doc_type FROM docs a LEFT join tasks b on b.id=a.task_id"
        sql2 = f" WHERE task_id IN {ids};"
        if id_type == "doc_id":
            if not no_single:
                sql2 = f" WHERE a.id IN {ids};"
            else:
                sql2 = f" WHERE task_id IN (SELECT task_id FROM docs WHERE id in {ids});"
        res = self._execute_by_select(sql=sql1 + sql2)
        return res
