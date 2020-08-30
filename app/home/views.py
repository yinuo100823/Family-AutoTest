# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/25 18:20
# @Author : Gery.li
# @File : views.py
from app.models import User
from . import home
from flask import render_template, session, g


@home.route("/")
def index():
    return render_template("home/index.html")


@home.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@home.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {"user_info": g.user}
    return {}
