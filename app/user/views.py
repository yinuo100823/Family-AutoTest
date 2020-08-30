# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/25 9:33
# @Author : Gery.li
# @File : views.py
from flask import render_template, redirect, \
    request, url_for, session, g, current_app

from app.forms import SignForm, LoginForm
from app.models import User
from . import user
from exts import db


@user.route("/user/sign/", methods=["GET", "POST"])
def sign():
    form = SignForm()
    if request.method == "POST" and form.validate_on_submit():
        telephone = form.telephone.data
        mini_name = form.mini_name.data
        password = form.password.data
        email = form.email.data
        new_user = User(telephone=telephone, mini_name=mini_name, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.login'))
    else:
        return render_template("user/sign.html", form=form)


@user.route("/user/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        telephone = form.telephone.data
        password = form.password.data
        remember = form.remember.data
        user_info = User.query.filter(User.telephone == telephone).first()

        if user_info and user_info.check_password(password):
            session["user_id"] = user_info.id
            if remember:
                session.permanent = True
            return redirect(url_for("home.index"))
        else:
            return render_template("user/login.html", error={"error": "用户不存在或密码错误！"}, form=form)
    else:
        return render_template("user/login.html", form=form)


@user.route("/logout/")
def logout():
    if hasattr(g, "user"):
        session.pop("user_id")
    return redirect(url_for("user.login"))


@user.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@user.context_processor
def context_processor():
    if hasattr(current_app, 'user'):
        return {"user_info": g.user}
    return {}
