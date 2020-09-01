# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/31 16:51
# @Author : Gery.li
# @File : CaseRun.py
import json
from .RequestUtil import RequestUtil
from exts import db

from app.models import Case


class CaseRun(RequestUtil):
    def __init__(self):
        super(CaseRun, self).__init__()

    def __assert_response(self, case, response):
        return {"is_pass": "success", "msg": "测试失败"}

    def run_case(self, id):
        case = Case.load_case_by_id(id)
        protocol = case.service.protocol
        host = case.service.host
        port = case.service.port
        if port:
            url = protocol + host + ":" + port + case.interface.uri
        else:
            url = protocol + host + case.interface.uri
        method = case.interface.method

        headers = json.loads(case.headers)
        for k, v in headers.items():
            if isinstance(v, dict):
                new_v = json.dumps(v)
                headers[k] = new_v
        body = json.loads(case.body)

        pre_case_id = case.pre_case_id
        pre_fields = json.loads(case.pre_fields)
        # 先判断是否存在前置case  todo
        # if pre_case_id:
        #     pre_case = Case.load_case_by_id(pre_case_id)
        #     pre_resp = Case.run_case(pre_case_id)
        #     if self.assert_response(pre_case, pre_resp) == "fail":
        #         pre_resp["msg"] = ".".join(["前置case：", pre_case.id, "-->", pre_case.name, "执行不通过"])
        #         return pre_resp
        #     # 提取case依赖的参数，pre_fields默认为[]
        #     for pre_param in pre_fields:
        #         pre_param_type = pre_param.get("scope")
        #         pre_param_name = pre_param.get("field")
        #         pre_param_value = pre_resp.get("data").get("pre_param_name")
        #         if pre_param_type == "header":
        #             headers[pre_param_name] = pre_param_value
        #         elif pre_param_type == "body":
        #             body[pre_param_name] = pre_param_value
        #         else:
        #             pass
        response = self.request(url=url, method=method, headers=headers, params=body)
        assert_result = self.__assert_response(case, response)
        case.is_pass = assert_result.get("is_pass")
        case.msg = assert_result.get("msg")
        case.resp = json.dumps(response, ensure_ascii=False)
        db.session.commit()
