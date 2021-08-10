#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/10 18:39
# @Author  : shangyameng@datagrand.com
# @Site    :
# @File    : idps_api.py


import json
import os
import re

from extensions.idps_tools.base import IdpsToolsBase


class IdpsTools(IdpsToolsBase):
    def __init__(self,
                 username="superadminpro",
                 password="BEgPDsMumFlc",
                 host="idps2-qyfw2.test.datagrand.cn",
                 port="80",
                 db_host="127.0.0.1",
                 db_port=21162,
                 db_user="root",
                 db_password="root",
                 db_database="contract",
                 charset="utf8mb4",
                 re_try=3,
                 product=True,
                 jumper_username="shangyameng"):
        super().__init__(username, password, host, port,
                         db_host, db_port, db_user, db_password, db_database, charset,
                         re_try, product, jumper_username)

    def create_request_by_single_file(self, file_path, type_name: str, ocr=True):
        """
        发起抽取任务
        Args:
            file_path: 文件位置
            type_name: 文档类型名字
            ocr: 是否使用OCR

        Returns:

        """
        self._login_by_user()
        self.logger.info(f"start request idps API.\t{os.path.basename(file_path)}")
        if type_name.isdecimal():
            type_id = type_name
        else:
            type_id, tags = self.get_tag_id_and_tags_by_tag_name(type_name)
        type_id = type_id if type_id else 1
        file = {"file": open(file_path, 'rb')}
        params = {"docType": int(type_id), "ocr": ocr}
        result = self._requests_processor(self.create_request_url,
                                          method="POST",
                                          params=params,
                                          file=file)
        return json.loads(result.content.decode("utf-8"))

    def get_table_extract_result(self, feature_type_id):
        """
        根据任务ID获取表格解析结果
        Args:
            feature_type_id: 任务ID

        Returns:
            表格解析返回的结果
        """
        self._login_by_user()
        url = self.get_table_result_url + feature_type_id
        result = self._requests_processor(url)
        return json.loads(result.content.decode("utf-8")) if result else None

    def get_tag_id_and_tags_by_tag_name(self, tag_name):
        """
        根据传入的tag_name获取该类型对应的ID
        Args:
            tag_name: 文档类型名字

        Returns:
            文档类型的ID
        """

        self._login_by_user()
        result = self._get_all_tag_types()
        all_tags = result.get("items", None) if result else None
        tag_type_id_list = [
            (item["id"], item["tags"]) for item in all_tags if item["name"] == tag_name
        ] if all_tags else None
        type_id = tag_type_id_list[0][0] if tag_type_id_list else None
        fields = tag_type_id_list[0][1] if tag_type_id_list else None
        return type_id, fields

    def request_ocr_url(self, file_path):
        """
        直接调用ocrd营业执照接口
        :param file_path:
        :return:
        """
        self.logger.info(f"start request OCR API.\t{os.path.basename(file_path)}")
        file = {"file": open(file_path, 'rb')}
        result = self._requests_processor(self.bizlicense,
                                          method="POST",
                                          file=file)
        return json.loads(result.content.decode("utf-8")) if result else None

    def create_fields_conf(self, save_file_path):
        """

        根据传入的文件类型生成extract抽取中的fields_conf.py文件
        :return:
        Args:
            save_file_path: 生成的fields_conf.py文件保存位置

        Returns:

        """

        all_fields_dict, all_fields_list, all_fields = {}, [], {}
        index, field_id, name = 1, "id", "name"
        write_info = """#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nfrom collections import namedtuple\n\nField = namedtuple('Field', ['id', 'name'])\n"""
        if save_file_path:
            if not os.path.exists(os.path.dirname(save_file_path)):
                os.makedirs(os.path.dirname(save_file_path))

            all_fields_list.sort(key=lambda x: x["id"])

            # 遍历所有tags
            for doctype in sorted(self.all_tags):
                doctype_tags = self.all_tags[doctype]
                for field in sorted(doctype_tags):
                    write_info += f"field{field} = Field('{field}', '{doctype_tags[field]}')" + "\n"

                    if doctype not in all_fields_dict.keys():
                        all_fields_dict[doctype] = [f"field{field}"]
                    else:
                        all_fields_dict[doctype].append(f"field{field}")

            # 生成all_fields
            var_info = "\n\nall_fields = {"
            var_info += ''.join([f"'*\n\t\t'{key}': [{', '.join(all_fields_dict[key])}],*'" for key in all_fields_dict])
            write_info += var_info + "\n\t\t}\n"

            # 写入文件
            with open(save_file_path, "w", encoding="utf-8") as f:
                f.write(re.sub(r"(?:'\*|\*')", "", write_info))

    def download_files(self, ids: list, file_save_path: str, id_type="task_id", file_type="json", more=True):
        """
        根据task_id，下载json文件到save_path
        Args:
            ids: 需要下载的文件的task_id对应的集合
            file_save_path:
            id_type: 传入的ID类型， 默认是task ID
            file_type: 需要下载的文件类型， 默认json
            more: 是否是多文件下载， 默认是多文件

        Returns:

        """
        if ids:
            res = self._select_files_uuid_by_id(ids=tuple(ids), id_type=id_type, no_single=more)
            self.logger.info(f"query number: ({len(res)}), result: {res}")
            if file_type == "json":
                file_name_1 = "_all.json"
                file_name_2 = "_ocr_all.json"
            elif file_type == "pdf":
                file_name_1 = ".pdf"
                file_name_2 = "_ocr.pdf"
            elif file_type == "txt":
                file_name_1 = ".txt"
                file_name_2 = "_ocr.txt"
            else:
                return

            for file_info in res:
                if file_info[-1] == 1:
                    file_name = re.sub(r"\.[a-zA-Z]+", file_name_1, file_info[0])
                elif file_info[-1] == 2:
                    file_name = re.sub(r"\.[a-zA-Z]+", file_name_2, file_info[0])
                else:
                    file_name = None
                file_url = self.download_file_url + file_name
                save_file_name = str(file_info[1]) + "_" + file_name
                self.logger.info(f"file name: {file_url}")
                response = self._requests_processor(file_url) if file_url else None
                self._save_file(response.content, save_file_name,
                                file_save_path, file_type) if response else None


if __name__ == "__main__":
    from config.extensions_conf import idps_config

    # test_file_path = "C:/Users/HSZH/Desktop/config_files/BOE TECHNOLOGY (HK) LIMITED/OR40102322000586/报关单.pdf"
    # save_path = "/Users/sarmn/Desktop/suyan_idps_fields_conf.py"
    # tasks_id = [280, 279, 278]
    # doc_id = [13]
    # saves_path = "/Users/sarmn/Nextcloud/code/idps小工具/upload"
    # saves_path = "/Users/sarmn/Desktop/EFI"

    with IdpsTools(idps_config) as idps_worker:
        # res = idps_worker.all_tags
        # res = idps_worker.get_tag_id_and_tags_by_tag_name("mas-安徽")
        # res = idps_worker.get_table_extract_result("2")
        # print(json.dumps(res, indent=4, ensure_ascii=False))
        # idps_worker.download_files(tasks_id, saves_path, id_type="doc_id", more=False, file_type="json")
        # res = idps_worker._requests_processor(
        #     "http://idps2-suyan-idps.datagrand.cn/upload/f5084de6-e6aa-11ea-8bc8-02420a01c794_ocr.pdf")
        # print(res.status_code)
        # print(res.content)
        file_path = "/Users/yangxiaobo/Downloads/企业名称登记申请书.pdf"
        res = idps_worker.create_request_by_single_file(file_path, "46")
        print(res)
        # print("s")
        # idps_worker.create_fields_conf(idps_config.upload / "file.py")
