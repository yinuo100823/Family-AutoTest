# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/25 18:20
# @Author : Gery.li
# @File : views.py
from app.models import User
from . import home
from flask import render_template
from flask_login import login_required


@home.route("/")
@login_required
def index():
    return render_template("home/index.html")
