# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/26 10:00
# @Author : Gery.li
# @File : __init__.py.py

from flask import Blueprint

services = Blueprint("services", __name__)
from . import views
