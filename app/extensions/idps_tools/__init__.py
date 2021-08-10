'''
# -*- coding: utf-8 -*-:
Version: 2.0
Autor: shangyameng
Date: 2021-03-17 12:22:33
LastEditors: shangyameng
LastEditTime: 2021-03-17 18:46:25
'''

from config.extensions_conf import idps_config
from .idps_api import IdpsApi

idps_tools_ = IdpsApi(idps_config)
