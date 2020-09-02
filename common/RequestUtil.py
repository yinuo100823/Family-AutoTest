# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/31 16:25
# @Author : Gery.li
# @File : RequestUtil.py
from requests import exceptions
import requests, json


class RequestUtil:
    def __init__(self):
        self.session = requests.session()

    def request(self, url, method, headers=None, params=None, content_type='application/json'):
        result = None
        try:
            if method == 'GET':
                result = self.session.get(url=url, params=params, headers=headers).json()
            elif method == 'POST':
                if content_type == 'application/json':
                    result = self.session.post(url=url, json=params, headers=headers).json()
                else:
                    result = self.session.post(url=url, data=params, headers=headers).json()
            elif method == "DELETE":
                result = self.session.delete(url=url, params=params, headers=headers).json()
            elif method == "PUT":
                result = self.session.put(url=url, params=params, headers=headers).json()
            else:
                print("http method not allowed")
            return result


        except exceptions.Timeout:

            return {'post请求出错': "请求超时"}

        except exceptions.InvalidURL:

            return {'post请求出错': "非法url"}

        except exceptions.HTTPError:

            return {'post请求出错': "http请求错误"}

        except Exception as e:

            return {'post请求出错': "错误原因:%s" % e}
