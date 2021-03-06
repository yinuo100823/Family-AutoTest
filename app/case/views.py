# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/25 18:21
# @Author : Gery.li
# @File : views.py
from datetime import datetime
from flask import render_template, request, url_for, g, redirect, flash
from exts import db
from . import case
from app.models import Case, Interface
from app.forms import CaseForm, CaseSearchForm, CaseAddForm
from common.CaseRun import CaseRun
from flask_login import login_required, current_user
from common.Constant import FlashEnum

select = "用例管理"
case_run = CaseRun()


@case.route("/case/list", methods=["GET", "POST"])
@login_required
def case_list():
    form = CaseSearchForm()
    cases = Case.query.filter(Case.creater_id == current_user.id).order_by(Case.update_time.desc())
    if request.method == "POST" and form.validate_on_submit():
        service = form.service.data
        interface = form.interface.data
        name = form.name.data
        if name:
            cases = [case for case in cases if case.name.find(name) != -1]
        if service:
            cases = [case for case in cases if case.service_id == service]
        if interface:
            cases = [case for case in cases if case.interface_id == interface]
        form.service.data = form.service.data
        form.interface.data = form.interface.data
        form.name.data = form.name.data
    return render_template("case/list.html", cases=cases, form=form, select=select)


@case.route("/case/<id>/info", methods=["GET", "POST"])
@login_required
def case_info(id):
    form = CaseForm()
    case = Case.query.filter(Case.id == id).first()
    if case:
        if request.method == "POST" and form.validate_on_submit():
            interface = Interface.query.filter(Interface.id == form.interface.data).first()
            case.interface = interface
            case.service = interface.service
            case.name = form.name.data
            case.is_run = form.is_run.data
            case.headers = form.headers.data
            case.body = form.body.data
            case.pre_case_id = form.pre_case_id.data if form.pre_case_id.data and form.pre_case_id.data != case.pre_case_id else None
            case.pre_fields = form.pre_fields.data
            case.except_result = form.except_result.data
            case.assert_type = form.assert_type.data
            case.update_time = datetime.now()
            case.is_pass = None
            case.msg = None
            case.resp = None
            try:
                db.session.commit()
                flash("保存成功", FlashEnum.success.name)
            except:
                flash("更新失败", FlashEnum.warning.name)
        else:
            form.interface.data = case.interface_id
            form.name.data = case.name
            form.is_run.data = case.is_run
            form.headers.data = case.headers
            form.body.data = case.body
            form.pre_case_id.data = case.pre_case_id
            form.pre_fields.data = case.pre_fields
            form.except_result.data = case.except_result
            form.assert_type.data = case.assert_type
            form.is_pass.data = case.is_pass
            form.msg.data = case.msg
            form.resp.data = case.resp
        return render_template("case/info.html", form=form, id=id, select=select)
    else:
        flash("您编辑的测试用例不存在", FlashEnum.warning.name)
        return redirect(url_for(".case_list"))


@case.route("/case/create/", methods=["GET", "POST"])
@login_required
def case_create():
    form = CaseAddForm()
    if request.method == "POST" and form.validate_on_submit():
        case = Case()
        interface = Interface.query.filter(Interface.id == form.interface.data).first()
        case.interface = interface

        case.service_id = interface.service_id
        case.name = form.name.data
        case.is_run = form.is_run.data
        case.headers = form.headers.data
        case.body = form.body.data
        case.pre_case_id = form.pre_case_id.data if form.pre_case_id.data else None
        case.pre_fields = form.pre_fields.data
        case.except_result = form.except_result.data
        case.creater_id = current_user.id
        case.assert_type = form.assert_type.data
        case.create_time = datetime.now()
        case.update_time = datetime.now()
        try:

            db.session.add(case)
            db.session.commit()
            flash("创建成功", FlashEnum.success.name)
        except:
            flash("创建失败", FlashEnum.warning.name)
        return redirect(url_for(".case_list"))
    else:
        return render_template("case/add.html", form=form, select=select)


@case.route("/case/<id>/copy/", methods=["POST"])
@login_required
def case_copy(id):
    try:
        case = Case.query.get(id)
        new_case = Case()
        new_case.service_id = case.service_id
        new_case.interface_id = case.interface_id
        new_case.name = case.name + "--复制"
        new_case.is_run = case.is_run
        new_case.headers = case.headers
        new_case.body = case.body
        new_case.pre_case_id = case.pre_case_id
        new_case.pre_fields = case.pre_fields
        new_case.except_result = case.except_result
        new_case.assert_type = case.assert_type
        new_case.creater_id = case.creater_id
        new_case.update_time = datetime.now()
        new_case.create_time = datetime.now()
        db.session.add(new_case)
        db.session.commit()
        flash("复制成功", FlashEnum.success.name)
    except:
        flash("由于字段过 or 数据库连接失败长导致复制失败", FlashEnum.danger.name)
    return redirect(url_for(".case_list"))


@case.route("/case/delete/", methods=["POST"])
@login_required
def case_delete():
    id = request.form.get("id")
    case = Case.query.get(id)
    if case:
        db.session.delete(case)
        db.session.commit()
        flash("删除成功", FlashEnum.success.name)
    return redirect(url_for(".case_list"))


@case.route("/case/<id>/run/", methods=["POST"])
@login_required
def case_run_by_id(id):
    is_pass, msg = case_run.run_case(id)
    if is_pass == "success":
        flash(msg, FlashEnum.success.name)
    else:
        flash(msg, FlashEnum.warning.name)
    if request.form.get("from_type") == "from_list":
        return redirect(url_for(".case_list"))
    return redirect(url_for(".case_info", id=id))


@case.route("/case/quick_search/", methods=["POST"])
@login_required
def case_quick_search():
    case_form = CaseSearchForm()
    cases = Case.query.filter(Case.creater_id == current_user.id).order_by(Case.update_time.desc())
    name = request.form.get("name")
    if name:
        cases = [case for case in cases if case.name.find(name) != -1]
        case_form.name.data = name
    return render_template("case/list.html", cases=cases, form=case_form, select=select)
