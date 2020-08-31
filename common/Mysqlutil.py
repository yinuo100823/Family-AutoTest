# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/6/2 10:02
# @Author : Gery.li
# @File : Mysqlutil.py
import pymysql
import config


class MysqlUtil:
    __obj = None
    __init_flag = True

    def __new__(cls, *args, **kwargs):
        if cls.__obj == None:
            cls.__obj = object.__new__(cls)
        return cls.__obj

    def __init__(self):  # 本地
        if MysqlUtil.__init_flag:
            self.__host = config.HOST
            self.__user = config.USERNAME
            self.__password = config.PASSWORD
            self.__port = config.PORT
            self.__connect = pymysql.connect(host=self.__host, user=self.__user, password=self.__password,
                                             port=self.__port)
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
