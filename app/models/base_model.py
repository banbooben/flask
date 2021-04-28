#!/usr/bin python3
# -*- coding: utf-8 -*-

# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2021-04-12 13:42:09
# @LastEditTime: 2021-04-12 14:40:50
# @FilePath: /app/models/base_model.py

from datetime import datetime

from sqlalchemy import BOOLEAN, DATETIME, INTEGER, Column, true

from initialization.extensions import db


class ActiveQuery:

    def __set__(self, instance):
        return

    def __get__(self, instance, owner):
        return owner.query.filter_by(active=True)


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(INTEGER, primary_key=True, autoincrement=True, comment="ID")
    active = Column(BOOLEAN, server_default=true(), nullable=False, comment="是否正常")
    create_time = Column(DATETIME, default=datetime.now, comment="修改时间")
    last_update_time = Column(DATETIME, default=datetime.now, onupdate=datetime.now, comment="最近修改时间", index=True)

    active_query = ActiveQuery()

    def auto_set_attr(self, **data):
        for k, v in data.items():
            if hasattr(self, k) and k != "id":
                setattr(self, k, v)
