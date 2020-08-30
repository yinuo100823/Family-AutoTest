# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from datetime import timedelta

# -----------数据库连接信息------------
# 数据库类型+驱动://username:password@host:port/database?charset=utf-8
DIALECT = "mysql"
DRIVER = "pymysql"
USERNAME = "root"
PASSWORD = "123456"
HOST = "localhost"
PORT = "3306"
DATABASE = "auto_test"
SQLALCHEMY_DATABASE_URI = "{0}+{1}://{2}:{3}@{4}:{5}/{6}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD,
                                                                              HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# session加密
SECRET_KEY = os.urandom(24)

# 是否开启debug模式
DEBUG = True
# session过期时间设置
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
