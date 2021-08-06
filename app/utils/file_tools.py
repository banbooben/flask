import json
import os
from pathlib import Path

from initialization.logger_process import logger


class FileTools(object):
    def __init__(self) -> None:
        ...

    def load_file(self) -> None:
        ...

    def load_all_files(self, dir_path_str) -> list:
        all_files_abs_path = []
        if not Path(dir_path_str).exists():
            return all_files_abs_path
        for root, _, files in os.walk(dir_path_str):
            for file in files:
                all_files_abs_path.append(os.path.join(root, file))
        return all_files_abs_path

    def save_to_file(self, data, save_path: str) -> None:
        if not data:
            data = b""
        if isinstance(data, bytes):
            write_type = "wb"
        else:
            write_type = "w"
            if isinstance(data, dict):
                data = json.dumps(data, ensure_ascii=False)
        try:
            if write_type == "w":
                with open(save_path, write_type, encoding="utf-8") as f:
                    f.write(data)
            else:
                with open(save_path, write_type) as f:
                    f.write(data)

        except Exception as e:
            logger.exception(e)
            logger.error(save_path)


if __name__ == '__main__':
    from utils.requests_tools import RequestTools
    from common.common_functions import get_uuid
    import time

    file_path = "C:/Users/sarmn/Downloads/a/b"
    save_file_path = "C:/Users/sarmn/Downloads/a/results"
    ysocr_url = "http://ysocr.datagrand.cn/ysocr/ocr"
    ysocr_file_url = "http://ysocr.datagrand.cn/file/"

    file_tools_ = FileTools()
    request_tools_ = RequestTools()

    all_files = file_tools_.load_all_files(file_path)
    all_files_res = file_tools_.load_all_files(save_file_path)
    all_files_res = [os.path.basename(file).rsplit(".", 1)[0] for file in all_files_res]
    for abs_file_path in all_files:
        file_name = os.path.basename(abs_file_path)
        if file_name.rsplit(".", 1)[0] in all_files_res:
            continue

        ocr_res_save_path = save_file_path + "/" + file_name.rsplit(".", 1)[0] + ".json"
        ocr_pdf_save_path = save_file_path + "/" + file_name.rsplit(".", 1)[0] + "_ocr.pdf"

        print(f"start file: {file_name} request")
        start_time = time.time()
        file = {"file": open(abs_file_path, 'rb')}
        data = {"caller_request_id": get_uuid()}
        resp = request_tools_.common_request_to_json(ysocr_url, method="post", files=file, params=data)
        if resp.get("code", 0) == 200:
            file_url = ysocr_file_url + resp.get("out_pdf_name")
            pdf_file = request_tools_.common_request(file_url).content
            file_tools_.save_to_file(resp, ocr_res_save_path)
            file_tools_.save_to_file(pdf_file, ocr_pdf_save_path)
            print(f"file: {file_name} is ok. use time {time.time() - start_time}")
    print("all_file is ok")
