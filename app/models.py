# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/25 9:29
# @Author : Gery.li
# @File : models.py
import json

from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from common.RequestUtil import RequestUtil


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
    protocol = db.Column(db.String(10), nullable=False, comment="协议：http、https")
    host = db.Column(db.String(50), nullable=False, index=True)
    port = db.Column(db.Integer)
    name = db.Column(db.String(50), nullable=False, index=True)
    desc = db.Column(db.Text)
    creater_id = db.Column(db.Integer, db.ForeignKey("bt_user.id"), nullable=False)
    creater = db.relationship("User", backref=db.backref("services"))
    create_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    update_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def __init__(self):
        self.__services = list()

    @property
    def services(self):
        self.__services.append((0, "请选择"))
        [self.__services.append((service.id, service.name + "（" + service.host + "）")) for service in
         Service.query.order_by(Service.id).all()]
        return self.__services


class Interface(db.Model):
    __tablename__ = 'bt_interface'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    uri = db.Column(db.String(50), nullable=False, comment="接口路径", index=True)
    name = db.Column(db.String(50), nullable=False, comment="接口名称", index=True)
    method = db.Column(db.String(10), nullable=False, comment="请求方式")
    headers = db.Column(db.String(200), nullable=False, comment="调用此接口时所需的headers信息")
    body = db.Column(db.Text, nullable=False, default="{}", comment="请求体")
    desc = db.Column(db.Text, comment="接口描述")
    env_type = db.Column(db.String(50), comment="环境类型：测试环境、开发环境、生产环境")
    creater_id = db.Column(db.Integer, db.ForeignKey("bt_user.id"), nullable=False)
    creater = db.relationship("User", backref=db.backref("interfaces"))
    service_id = db.Column(db.Integer, db.ForeignKey("bt_service.id"), nullable=False)
    service = db.relationship("Service", backref=db.backref("interfaces"))  # 接口所属服务
    create_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    update_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def __init__(self):
        self.__interfaces = list()

    @property
    def interfaces(self):
        self.__interfaces.append((0, "请选择"))
        [self.__interfaces.append((interface.id, interface.name + "（" + interface.uri + "）")) for interface in
         Interface.query.order_by(Interface.id).all()]
        return self.__interfaces


class Case(db.Model):
    __tablename__ = 'bt_case'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    service_id = db.Column(db.Integer, db.ForeignKey("bt_service.id"), nullable=False, index=True)
    service = db.relationship("Service", backref=db.backref("cases"))  # case所属服务
    interface_id = db.Column(db.Integer, db.ForeignKey("bt_interface.id"), nullable=False, comment="关联的接口")
    interface = db.relationship("Interface", backref=db.backref("cases"))
    name = db.Column(db.String(50), nullable=False, comment="测试用例名称")
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

    def __init__(self):
        self.__cases = list()

    @property
    def cases(self):
        self.__cases.append((0, "请选择"))
        [self.__cases.append((case.id, case.name)) for case in
         Case.query.order_by(Case.id).all()]
        return self.__cases

    @classmethod
    def load_cases_by_app(cls, service_id):
        return Case.query.filter(Case.service_id == service_id).all()

    @classmethod
    def load_case_by_id(cls, case_id):
        return Case.query.filter(Case.id == case_id).first()

    @classmethod
    def load_cases_by_user(cls, user_id):
        return Case.query.filter(Case.creater_id == user_id).all()

    @classmethod
    def update_result_by_id(cls, case_id, is_pass, msg, resp):
        case = cls.load_case_by_id(case_id)
        case.update_time = datetime.now()
        case.is_pass = is_pass
        case.msg = msg
        case.resp = resp
        db.session.commit()

    # @classmethod
    # def assert_response(cls, case, response):
    #     return {"is_pass": "success", "msg": None}
    #
    # @classmethod
    # def run_case(cls, id):
    #     req = RequestUtil()
    #     case = Case.load_case_by_id(id)
    #     host = case.service.host
    #     port = case.service.port
    #     if port:
    #         url = host + ":" + port + case.interface.uri
    #     else:
    #         url = host + case.interface.uri
    #     method = case.interface.method
    #     headers = json.loads(case.headers)
    #     body = json.loads(case.body)
    #     pre_case_id = case.pre_case_id
    #     pre_fields = json.loads(case.pre_fields)
    #     # 先判断是否存在前置case
    #     if pre_case_id:
    #         pre_case = cls.load_case_by_id(pre_case_id)
    #         pre_resp = cls.run_case(pre_case_id)
    #         if cls.assert_response(pre_case, pre_resp) == "fail":
    #             pre_resp["msg"] = ".".join(["前置case：", pre_case.id, "-->", pre_case.name, "执行不通过"])
    #             return pre_resp
    #         # 提取case依赖的参数，pre_fields默认为[]
    #         for pre_param in pre_fields:
    #             pre_param_type = pre_param.get("scope")
    #             pre_param_name = pre_param.get("field")
    #             pre_param_value = pre_resp.get("data").get("pre_param_name")
    #             if pre_param_type == "header":
    #                 headers[pre_param_name] = pre_param_value
    #             elif pre_param_type == "body":
    #                 body[pre_param_name] = pre_param_value
    #             else:
    #                 pass
    #     response = req.request(url=url, method=method, headers=headers, params=body)
    #     return response

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
