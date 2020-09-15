# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/26 9:21
# @Author : Gery.li
# @File : views.py
from datetime import datetime

from flask_login import current_user, login_required

from app.forms import InterfaceForm, InterfaceSearchForm
from . import interface
from flask import render_template, g, request, flash, redirect, url_for
from app.models import Interface
from sqlalchemy import and_
from exts import db

select = "接口管理"


@interface.route("/interface/list", methods=["GET", "POST"])
@login_required
def interface_list():
    form = InterfaceSearchForm()
    interfaces = Interface.query.filter(Interface.creater_id == current_user.id).order_by(Interface.update_time.desc())
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        uri = form.uri.data
        service = form.service.data

        if name:
            interfaces = [interface for interface in interfaces if interface.name.find(name) != -1]
            form.name.data = form.name.data
        if uri:
            interfaces = [interface for interface in interfaces if interface.uri.find(uri) != -1]
            form.uri.data = form.uri.data
        if service:
            interfaces = [interface for interface in interfaces if interface.service_id == service]
            form.service.data = form.service.data
    return render_template("interface/list.html", interfaces=interfaces, form=form, select=select)


@interface.route("/interface/<id>/info", methods=["GET", "POST"])
@login_required
def interface_info(id):
    form = InterfaceForm()
    interface = Interface.query.filter(and_(Interface.id == id, Interface.creater_id == current_user.id)).first()
    if interface:
        if request.method == "POST" and form.validate_on_submit():
            interface.name = form.name.data
            interface.uri = form.uri.data
            interface.method = form.method.data
            interface.headers = form.headers.data
            interface.body = form.body.data
            interface.service_id = form.service.data
            interface.desc = form.desc.data
            interface.update_time = datetime.now()
            db.session.commit()
            return redirect(url_for(".interface_list"))
        else:
            form.name.data = interface.name
            form.uri.data = interface.uri
            form.method.data = interface.method
            form.headers.data = interface.headers
            form.body.data = interface.body
            form.service.data = interface.service_id
            form.desc.data = interface.desc
        return render_template("interface/info.html", form=form, id=id, select=select)
    else:
        return


@interface.route("/interface/create/", methods=["GET", "POST"])
@login_required
def interface_create():
    form = InterfaceForm()
    if request.method == "POST" and form.validate_on_submit():
        interface = Interface()
        interface.name = form.name.data
        interface.uri = form.uri.data
        interface.method = form.method.data
        interface.headers = form.headers.data
        interface.body = form.body.data
        interface.service_id = form.service.data
        interface.desc = form.desc.data
        interface.creater_id = current_user.id
        interface.create_time = datetime.now()
        interface.update_time = datetime.now()
        interface.env_type = "测试环境"
        db.session.add(interface)
        db.session.commit()
        return redirect(url_for(".interface_list"))
    else:
        return render_template("interface/add.html", form=form, select=select)
