# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/27 12:00 上午
# @Name    : manage.py
# @Desc    :

from flask_script import Manager

from flask_migrate import MigrateCommand
from flask import jsonify
from initialization import init_app
from config.extensions_conf import HTTP_HOST, HTTP_PORT

from initialization.application import logger
from initialization.error_process import ExtractException

app = init_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route("/", methods=['GET'])
def index():
    logger.info("ok test")
    logger.error("error test")
    logger.debug("debug test")
    # raise ExtractException(code="E02")
    return jsonify({"code": 200, "msg": "ok", "data": {}})


if __name__ == "__main__":
    app.run(host=HTTP_HOST, port=HTTP_PORT, debug=True)
    # a = ""
    # manager.run()
