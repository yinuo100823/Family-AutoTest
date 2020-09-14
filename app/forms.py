# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/25 9:29
# @Author : Gery.li
# @File : forms.py
import json

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, \
    IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Length, Optional
from app.models import Service, User, Interface, Case
from wtforms import ValidationError


class RenderForm(FlaskForm):
    class Meta(FlaskForm.Meta):
        """
        重写render_field，实现Flask-Bootstrap与render_kw的class并存
        """

        def render_field(self, field, render_kw):
            other_kw = getattr(field, 'render_kw', None)
            if other_kw is not None:
                class1 = other_kw.get('class', None)
                class2 = render_kw.get('class', None)
                if class1 and class2:
                    render_kw['class'] = class2 + ' ' + class1
                render_kw = dict(other_kw, **render_kw)
            return field.widget(field, **render_kw)


class SignForm(RenderForm):
    telephone = StringField("手机号码", validators=[DataRequired(), Length(max=11, min=11)],
                            render_kw={"placeholder": "手机号码"})
    mini_name = StringField("昵称", validators=[DataRequired(), Length(max=6)])
    email = StringField("电子邮箱", validators=[DataRequired(), Email()])
    password = PasswordField("密码", validators=[DataRequired(), Length(min=6, max=10)])
    re_password = PasswordField("重复密码", validators=[DataRequired(), EqualTo("password", message="两次密码输入不一致")])

    submit = SubmitField("立即注册", render_kw={"class": "btn-primary btn-block"})

    # 验证邮箱和手机号是否已被注册
    def validate_email(self, field):
        if User.query.filter(User.email == field.data).first():
            raise ValidationError("邮箱已被注册")

    def validate_telephone(self, field):
        if User.query.filter(User.telephone == field.data).first():
            raise ValidationError("手机号已被注册")


class LoginForm(RenderForm):
    telephone = StringField("手机号码", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("记住我")
    submit = SubmitField("立即登陆", render_kw={"class": "btn-primary btn-block"})

    # 验证用户名是否存在
    def validate_telephone(self, field):
        if not User.query.filter(User.telephone == field.data).first():
            raise ValidationError("手机号:{0}尚未注册，快去注册吧!".format(field.data))


class ServiceForm(RenderForm):
    name = StringField("应用名称", validators=[DataRequired(), Length(max=50)])
    protocol = SelectField("协议", choices=[("http", "http"), ("https", "https")])
    host = StringField("应用地址", validators=[DataRequired(), Length(max=50)])
    port = IntegerField("应用端口", validators=[Optional()])
    desc = TextAreaField("应用描述")
    submit = SubmitField("保存", render_kw={"class": "btn-primary btn-block"})


class InterfaceForm(RenderForm):
    service = SelectField("所属应用", coerce=int)
    name = StringField("接口名称", validators=[DataRequired(), Length(max=50)])
    uri = StringField("接口路径", validators=[DataRequired(), Length(max=50)])
    method = SelectField('*请求方式', choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')])
    headers = TextAreaField("请求头", validators=[DataRequired(), Length(max=500)], default={})
    body = TextAreaField("*请求体(body)", validators=[DataRequired()], render_kw={"rows": 15}, default={})
    desc = TextAreaField("接口描述")

    submit = SubmitField("保存", render_kw={"class": "btn-primary btn-block"})

    def __init__(self, *args, **kwargs):
        super(InterfaceForm, self).__init__(*args, **kwargs)
        self.service.choices = Service().services

    def validate_service(self, field):
        if field.data == 0:
            raise ValidationError("接口所属应用必选")


class CaseAddForm(RenderForm):
    interface = SelectField("* 所测接口", coerce=int)
    name = StringField("* 测试用例名称", validators=[DataRequired(), Length(max=100)])
    is_run = SelectField('* 是否执行', choices=[('Yes', 'Yes'), ('No', 'No')])
    headers = TextAreaField("* 请求头(headers)", validators=[DataRequired()],
                            render_kw={"rows": 2, "id": "request-header"})
    body = TextAreaField("* 请求体(body)", validators=[DataRequired()], render_kw={"rows": 15, "id": "request-body"})
    pre_case_id = SelectField("依赖的测试用例", coerce=int, choices=[])
    pre_fields = TextAreaField("前置数据设置（必须是Json格式）", render_kw={"rows": 10, "id": "request-pre-fields"})
    assert_type = TextAreaField('*断言类型（{"type":"resp.data","field":"field_name"}，必须是Json格式）',
                                validators=[DataRequired()],
                                render_kw={
                                    "placeholder": '{"type":断言类型（目前支持resp.data,resp.dataArray,resp.code）'
                                                   ',"field":断言的字段名称}'})
    except_result = TextAreaField('* 预期结果({"type":"!=、==、>、<","value":"None"}，必须是Json格式)', validators=[DataRequired()],
                                  render_kw={
                                      "placeholder": '{"type":"!=、=、>、<","content":"None"}==>type:比较的方式；value:比较的内容'})
    submit = SubmitField("保存", render_kw={"class": "btn-primary btn-block"})

    def __init__(self, *args, **kwargs):
        super(CaseAddForm, self).__init__(*args, **kwargs)
        self.interface.choices = Interface().interfaces
        self.pre_case_id.choices = Case().cases

    # 验证Json格式的字段
    def validate_interface(self, field):
        if field.data == 0:
            raise ValidationError("所测接口必选")

    def validate_headers(self, field):
        try:
            json.loads(field.data)
        except:
            raise ValidationError("headers必须为Json格式")

    def validate_body(self, field):
        try:
            json.loads(field.data)
        except:
            raise ValidationError("body必须为Json格式")

    def validate_pre_fields(self, field):
        try:
            json.loads(field.data)
        except:
            raise ValidationError("前置数据必须为Json格式")

    def validate_assert_type(self, field):
        try:
            json.loads(field.data)
        except:
            raise ValidationError("断言类型必须为Json格式")

    def validate_except_result(self, field):
        try:
            json.loads(field.data)
        except:
            raise ValidationError("预期结果必须为Json格式")


class CaseForm(CaseAddForm):
    is_pass = StringField("调试是否通过", render_kw={"disabled": "disabled"})
    msg = StringField(label="调试的错误信息", render_kw={"disabled": "disabled"})
    resp = TextAreaField("调试返回response", render_kw={"disabled": "disabled"})
    submit = SubmitField("保存(成功后将清除调试信息)", render_kw={"class": "btn-primary btn-block"})

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)


class CaseSearchForm(RenderForm):
    name = StringField("测试用例名称:")
    service = SelectField("所属应用:", coerce=int, choices=[])
    interface = SelectField("测试接口:", coerce=int, choices=[])
    submit = SubmitField("搜索", render_kw={"class": "btn-primary"})

    def __init__(self, *args, **kwargs):
        super(CaseSearchForm, self).__init__(*args, **kwargs)
        self.interface.choices = Interface().interfaces
        self.service.choices = Service().services


class InterfaceSearchForm(RenderForm):
    name = StringField("接口名称:")
    uri = StringField("接口路径:")
    service = SelectField("所属应用:", coerce=int, choices=[])
    submit = SubmitField("搜索", render_kw={"class": "btn-primary"})

    def __init__(self, *args, **kwargs):
        super(InterfaceSearchForm, self).__init__(*args, **kwargs)
        self.service.choices = Service().services
