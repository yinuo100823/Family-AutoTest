# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/25 9:28
# @Author : Gery.li
# @File : __init__.py.py
from flask import Blueprint

home = Blueprint("home", __name__)
from . import views