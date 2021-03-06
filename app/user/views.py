# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/25 9:33
# @Author : Gery.li
# @File : views.py
from flask import render_template, redirect, \
    request, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import SignForm, LoginForm
from app.models import User
from common.Constant import FlashEnum
from . import user
from exts import db


@user.route("/user/sign/", methods=["GET", "POST"])
def sign():
    # form = SignForm()
    # if request.method == "POST" and form.validate_on_submit():
    if request.method == "POST":
        telephone = request.form.get("telephone")
        mini_name = request.form.get("mini_name")
        password = request.form.get("password")
        email = request.form.get("email")
        new_user = User(telephone=telephone, mini_name=mini_name, password=password, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            flash("注册用户失败",FlashEnum.warning.name)
        return redirect(url_for('.login'))
    return render_template("user/user.html")


@user.route("/user/login/", methods=["GET", "POST"])
def login():
    # form = LoginForm()
    if request.method == "POST":
        telephone = request.form.get("telephone")
        password = request.form.get("password")
        remember = request.form.get("remember")
        user_info = User.query.filter(User.telephone == telephone).first()

        if user_info and user_info.check_password(password):
            login_user(user_info, remember)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("index")
                return redirect(next)
        flash("用户不存在或密码错误！", FlashEnum.warning.name)
    return render_template("user/user.html")


@user.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("退出成功", FlashEnum.success.name)
    return redirect(url_for(".login"))

# @user.before_app_request
# def before_request():
#     g.user = current_user


# @user.context_processor
# def context_processor():
#     if hasattr(g, 'user'):
#         return {"user_info": g.user}
#     return {}
