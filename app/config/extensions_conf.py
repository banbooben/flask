#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/2 18:57
# @Author  : shangyameng@aliyun.com
# @Site    :
# @File    : extensions_conf.py

import os
from pathlib import Path

# http config
HTTP_HOST = '0.0.0.0'
HTTP_PORT = 5000

# header config
fake_useragent_file_path = "/Users/sarmn/import_files/fake_useragent_0.1.11.json"

# aria config
aria_host = "127.0.0.1"
aria_port = "6800"
aria_token = "test"


class IdpsConfig(object):
    # 接口接收的文件保存的文件夹
    upload = Path().cwd() / "static/upload"

    # idps登录使用账号密码
    username = "superadminpro"
    password = "BEgPDsMumFlc"

    # 登录失败后重试次数
    re_try = 3

    # idps部署信息
    host = "idps2-qyfw2.test.datagrand.cn"
    # "host = "idps2-qyfw2.datagrand.cn"
    port = "80"

    # 接口路由信息
    logon_route = "api/login"  # 登录接口
    creat_request_route = "api/extracting/instant"  # 文件抽取
    get_extract_result_route = "api/web_api/table/"  # 表格抽取
    tag_types_route = "api/tag_types"

    test_id = "?id=158"  # 解析工具ID
    tag_types_key = "?start=0&number=1000"

    # 数据库信息
    db_host = "127.0.0.1"
    db_port = 21162
    # "db_port = 21169
    db_user = "root"
    db_password = "root"
    db_database = "contract"
    charset = "utf8mb4"

    product = True


class OcrConfig(object):
    """OCR配置"""

    ocr_url = os.getenv("OCR_URL", "http://ysocr.datagrand.cn/ysocr/ocr")
    ocr_file = os.getenv("OCR_FILE", "http://ysocr.datagrand.cn/file/")

    word2pdf_fields = ['doc', "docx", 'xls', 'xlsx']
    ocr_file_suffix = ["pdf", "jpeg", "jpg", "png", "PDF", "JPG", "JPEG", "PNG"]


ocr_config = OcrConfig()

idps_config = IdpsConfig()
