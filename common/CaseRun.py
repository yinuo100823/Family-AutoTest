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

    def __assert_response(self, case: Case, response: dict):
        is_pass = "fail"  # 是否断言成功的标志
        msg = ""
        try:
            assert_type = json.loads(case.assert_type)
            except_result = json.loads(case.except_result)
            # 如果要判断是不是None，需要把字符串“none”，替换成None对象
            if isinstance(except_result.get("value"), str) and except_result.get("value").upper() == "NONE":
                except_result["value"] = None
        except Exception as e:
            msg = "前置数据 or 断言类型 or 预期结果json解析失败，请确认格式，{0}".format(e.args)
            return {"is_pass": is_pass, "msg": msg}
        _assert_type = assert_type.get("type")
        # 根据不同的断言类型，分别获取response中的内容，用来和预期结果比较
        if _assert_type == "resp.data":
            _resp_data = response.get(assert_type.get("field"))
        elif _assert_type == "resp.dataArray":
            _resp_data = len(response.get(assert_type.get("field")))
        elif _assert_type == "resp.code":
            _resp_data = response.get(assert_type.get("field"))
        else:
            msg = "暂不支持的断言类型：{0}".format(_assert_type)
            return {"is_pass": is_pass, "msg": msg}
        comp_type = except_result.get("type")
        comp_value = except_result.get("value")
        if comp_type == ">" or comp_type == "<":
            try:
                comp_value = float(comp_value)
            except:
                msg = "填写的比较类型为：{0}时，value【{1}】必须为{2}".format(comp_type, comp_value, "数字类型")
                return {"is_pass": is_pass, "msg": msg}
        # 根据比较类型进行 resp和预期结果的比较
        if comp_type == "!=":
            is_pass = "success" if _resp_data is not comp_value else is_pass
        elif comp_type == "==" or "=":
            is_pass = "success" if _resp_data == comp_value else is_pass
        elif comp_type == ">":
            is_pass = "success" if _resp_data > comp_value else is_pass
        elif comp_type == "<":
            is_pass = "success" if _resp_data < comp_value else is_pass
        else:
            msg = "填写的比较类型：{0}暂不支持".format(comp_type)
            return {"is_pass": is_pass, "msg": msg}

        if is_pass == "fail":
            msg = "{0}  {1}  {2},断言失败".format(_resp_data, comp_type, comp_value)
        return {"is_pass": is_pass, "msg": msg}

    def run_case(self, id):
        case = Case.load_case_by_id(id)
        protocol = case.service.protocol
        host = case.service.host
        port = case.service.port
        url = protocol + "://" + host + ":" + port + case.interface.uri if port else protocol + "://" + host + case.interface.uri
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
