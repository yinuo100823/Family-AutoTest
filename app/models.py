# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/25 9:29
# @Author : Gery.li
# @File : models.py

from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = 'bt_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    telephone = db.Column(db.String(11), nullable=False, index=True)
    mini_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, index=True)
    create_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    # 密码加密，需要：from werkzeug.security import generate_password_hash
    def __init__(self, *args, **kwargs):
        self.telephone = kwargs.get("telephone")
        self.mini_name = kwargs.get("mini_name")
        self.password = generate_password_hash(kwargs.get("password"))
        self.create_time = kwargs.get("create_time")
        self.email = kwargs.get("email")

    # 检查密码是否正确：check_password_hash
    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


# 服务模型
class Service(db.Model):
    __tablename__ = 'bt_service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    host = db.Column(db.String(50), nullable=False, index=True)
    port = db.Column(db.Integer)
    name = db.Column(db.String(50), nullable=False, index=True)
    desc = db.Column(db.Text)
    creater_id = db.Column(db.Integer, db.ForeignKey("bt_user.id"), nullable=False)
    creater = db.relationship("User", backref=db.backref("services"))
    create_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    update_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())




class Interface(db.Model):
    __tablename__ = 'bt_interface'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    uri = db.Column(db.String(50), nullable=False, comment="接口路径", index=True)
    name = db.Column(db.String(50), nullable=False, comment="接口名称", index=True)
    headers = db.Column(db.String(200), nullable=False, comment="调用此接口时所需的headers信息")
    desc = db.Column(db.Text, comment="接口描述")
    env_type = db.Column(db.String(50), comment="环境类型：测试环境、开发环境、生产环境")
    creater_id = db.Column(db.Integer, db.ForeignKey("bt_user.id"), nullable=False)
    creater = db.relationship("User", backref=db.backref("interfaces"))
    service_id = db.Column(db.Integer, db.ForeignKey("bt_service.id"), nullable=False)
    service = db.relationship("Service", backref=db.backref("interfaces"))  # 接口所属服务
    create_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    update_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())


class Case(db.Model):
    __tablename__ = 'bt_case'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    service_id = db.Column(db.Integer, db.ForeignKey("bt_service.id"), nullable=False, index=True)
    service = db.relationship("Service", backref=db.backref("cases"))  # case所属服务
    interface_id = db.Column(db.Integer, db.ForeignKey("bt_interface.id"), nullable=False, comment="关联的接口")
    interface = db.relationship("Interface", backref=db.backref("cases"))
    name = db.Column(db.String(50), nullable=False, comment="测试用例名称")
    method = db.Column(db.String(10), nullable=False, comment="请求方式")
    is_run = db.Column(db.String(3), nullable=False, comment="是否运行：Yes/No", default="Yes")
    headers = db.Column(db.Text, default={}, comment="接口时所需的headers信息")
    body = db.Column(db.Text, default={}, comment="请求body")
    pre_case_id = db.Column(db.Integer, default=None, comment="依赖的前置case")
    pre_fields = db.Column(db.Text, default="", comment="前置的字段, 获取请求结果的哪个字段，用于当前case的header还是body,双&name& 替代值")
    except_result = db.Column(db.Text, default="", nullable=False, comment="预期结果")
    assert_type = db.Column(db.Text, nullable=False, comment="断言类型,:判断状态码、data内容或数组长度等，后期考虑从数据库读取数据进行验证")
    is_pass = db.Column(db.String(10), default="", comment="最后一次运行的成功/失败的状态")
    msg = db.Column(db.Text, default="", comment="最后一次运行的成功/失败的状态")
    resp = db.Column(db.Text, default="", comment="最后一次运行的返回结果")
    creater_id = db.Column(db.Integer, db.ForeignKey("bt_user.id"), nullable=False)
    creater = db.relationship("User", backref=db.backref("cases"))
    create_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    update_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())


# ---------------------------------多对多关系-----------------------------------------
# product_tag = db.Table(
#     "bt_product_tag_relation",  # 表名称
#     db.Column("product_id", db.Integer, db.ForeignKey("bt_product.id"), primary_key=True),
#     db.Column("tag_id", db.Integer, db.ForeignKey("bt_tag.id"), primary_key=True)
# )
#
#
# class Product(db.Model):
#     __tablename__ = "bt_product"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100), nullable=False)
#     # secondary=product_tag:中间表，即product和tag的关系表
#     tags = db.relationship("Tag", secondary=product_tag, backref=db.backref("products"))
#
#
# class Tag(db.Model):
#     __tablename__ = "bt_tag"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(100), nullable=False)