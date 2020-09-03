# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/26 10:01
# @Author : Gery.li
# @File : views.py
from datetime import datetime
from operator import and_

from flask import render_template, redirect, url_for, g, request, flash
from sqlalchemy import and_
from app.models import Service
from app.forms import ServiceForm
from exts import db
from flask_login import login_required, current_user

from . import services

select = "服务管理"


@services.route("/service/list")
@login_required
def service_list():
    name = request.args.get("name")
    host = request.args.get("host")
    user_id = current_user.id
    if name and host:
        search = and_(Service.creater_id == user_id, Service.name.contains(name),
                      Service.host.contains(host))
    elif name:
        search = and_(Service.creater_id == user_id, Service.name.contains(name))
    elif host:
        search = and_(Service.creater_id == user_id, Service.host.contains(host))
    else:
        search = and_(Service.creater_id == user_id)
    services = Service.query.filter(search).order_by(Service.update_time.desc())
    return render_template("services/list.html", services=services, select=select)


@services.route("/services/<id>/info", methods=["GET", "POST"])
@login_required
def service_info(id):
    form = ServiceForm()
    service = Service.query.filter(and_(Service.id == id)).first()
    if service:
        if request.method == "POST" and form.validate_on_submit():
            service.name = form.name.data
            service.protocol = form.protocol.data
            service.host = form.host.data
            service.port = form.port.data
            service.desc = form.desc.data
            service.update_time = datetime.now()
            db.session.commit()
            return redirect(url_for(".service_list"))
        form.name.data = service.name
        form.host.data = service.host
        form.port.data = service.port
        form.desc.data = service.desc
        form.protocol.data = service.protocol
        return render_template("services/info.html", form=form, id=id, select=select)
    flash("查看的服务不存在，请重试")
    return redirect(url_for(".service_list"))


@services.route("/service/create/", methods=["GET", "POST"])
@login_required
def service_create():
    form = ServiceForm()
    if request.method == "POST" and form.validate_on_submit():
        service = Service()
        service.name = form.name.data
        service.host = form.host.data
        service.port = form.port.data
        service.desc = form.desc.data
        service.protocol = form.protocol.data
        service.creater_id = current_user.id
        service.create_time = datetime.now()
        service.update_time = datetime.now()
        try:
            db.session.add(service)
            db.session.commit()
        except Exception as e:
            flash("创建服务失败，请重试")
        return redirect(url_for(".service_list"))
    return render_template("services/add.html", form=form, select=select)

