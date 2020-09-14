# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/6/2 10:02
# @Author : Gery.li
# @File : Mysqlutil.py
import datetime
import pymysql


class MysqlUtil:
    __obj = None
    __init_flag = True

    def __new__(cls, *args, **kwargs):
        if cls.__obj == None:
            cls.__obj = object.__new__(cls)
        return cls.__obj

    def __init__(self, env="local"):
        if MysqlUtil.__init_flag:
            if env == "local":
                self.__connect = pymysql.connect(host="localhost", user="root", password="123456", port=3306)
            elif env == "production":
                self.__connect = pymysql.connect(host="10.0.0.59", user="app_vo_open", password="Tz23Zd112#1",
                                                 port=8989)

            else:
                self.__connect = pymysql.connect(host="10.0.0.76", user="app", password="ZAQ!2wsx", port=3306)

            self.__cursor = self.__connect.cursor()
            MysqlUtil.__init_flag = False

    def insert(self, sql, params=None):
        count = 0
        if isinstance(params, list):
            count = self.__cursor.executemany(sql, params)
        elif isinstance(params, tuple):
            count = self.__cursor.execute(sql, params)
        return count

    def delete(self, sql, params=None):
        return self.__cursor.execute(sql, params)

    def update(self, sql, params=None):
        return self.__cursor.execute(sql, params)

    def select(self, sql, params=None, size=None):
        result = None
        self.__cursor.execute(sql, params)
        if not size:
            result = self.__cursor.fetchall()
        elif size == 1:
            result = self.__cursor.fetchone()
        else:
            result = self.__cursor.fetchmany(size=size)
        return result

    def close(self):
        self.__connect.close()
        self.__cursor = None

    def commit(self):
        self.__connect.commit()

    def rollback(self):
        self.__connect.rollback()
