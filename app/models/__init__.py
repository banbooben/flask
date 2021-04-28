# !/usr/bin/env python
# coding:utf-8
# @Time    : 2020/12/26 11:48 下午
# @Contact : shangyameng
# @Name    : __init__.py.py
# @Desc    :

from initialization.extensions import db
from .user_model import UserModel

# def init_db():
# db.create_all()

__all__ = ["UserModel"]




