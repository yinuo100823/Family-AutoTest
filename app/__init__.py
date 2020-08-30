# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/25 9:25
# @Author : Gery.li
# @File : __init__.py.py

from flask import Flask
from flask_bootstrap import Bootstrap
import config
from .home import home as home_blueprint
from .user import user as user_blueprint
from .case import case as case_blueprint
from .interface import interface as interface_blueprint
from .services import services as services_blueprint
from exts import db


bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    bootstrap.init_app(app)
    db.init_app(app)

    # 添加路由和自定义的错误页面

    # 注册蓝本
    app.register_blueprint(home_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(case_blueprint)
    app.register_blueprint(interface_blueprint)
    app.register_blueprint(services_blueprint)
    return app
