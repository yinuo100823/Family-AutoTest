# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/20 12:35
# @Author : Gery.li
# @File : manage.py
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from exts import db
from flasky import app
from app.models import User,Service,Interface,Case

"""
在终端执行三个命令进行数据Model的迁移：
python manage.py db init：   初始化一个迁移的环境---只需要做一次
python manage.py db migrate：准备迁移的数据文件
python manage.py db upgrade：实行迁移操作，把Model真正映射到数据库中 

"""
manage = Manager(app)

# 使用flask_migrate必须绑定app和db
migrate = Migrate(app, db)
# 把MigrateCommand添加到manage中
manage.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manage.run()
