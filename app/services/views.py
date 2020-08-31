# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/26 10:01
# @Author : Gery.li
# @File : views.py
from datetime import datetime
from operator import and_

from flask import render_template, redirect, url_for, session, g, request
from sqlalchemy import and_
from app.models import User, Service
from app.forms import ServiceForm, LoginForm
from exts import db
from flasky import logging

from . import services


@services.route("/service/list")
def service_list():
    name = request.args.get("name")
    host = request.args.get("host")
    user_id = g.user.id
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
    return render_template("services/list.html", services=services)


@services.route("/services/<id>/info", methods=["GET", "POST"])
def service_info(id):
    form = ServiceForm()
    service = Service.query.filter(and_(Service.id == id, Service.creater_id == g.user.id)).first()
    if service:
        if request.method == "POST" and form.validate_on_submit():
            service.name = form.name.data
            service.host = form.host.data
            service.port = form.port.data
            service.desc = form.desc.data
            service.update_time = datetime.now()
            db.session.commit()
            return redirect(url_for(".service_list"))
        else:
            form.name.data = service.name
            form.host.data = service.host
            form.port.data = service.port
            form.desc.data = service.desc
        return render_template("services/info.html", form=form, id=id)
    else:
        logging.error("编辑的服务信息不存在")
        return


@services.route("/service/create/", methods=["GET", "POST"])
def service_create():
    form = ServiceForm()
    if request.method == "POST" and form.validate_on_submit():
        service = Service()
        service.name = form.name.data
        service.host = form.host.data
        service.port = form.port.data
        service.desc = form.desc.data
        service.creater_id = g.user.id
        service.create_time = datetime.now()
        service.update_time = datetime.now()
        db.session.add(service)
        db.session.commit()
        return redirect(url_for(".service_list"))
    else:
        return render_template("services/add.html", form=form)


@services.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user
    else:
        return render_template("user/login.html", form=LoginForm())


@services.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {"user_info": g.user}
    return {}
