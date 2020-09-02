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
        assert_type = None
        except_result = None
        is_pass = "fail"  # 是否断言成功的标志
        msg = ""
        _assert_content = None  # 需要和预期结果对比的内容，不同的断言类型，内容不一样
        try:
            assert_type = json.loads(case.assert_type)
            except_result = json.loads(case.except_result)
            if isinstance(except_result.get("content"), str) and except_result.get("content").upper() == "NONE":
                except_result["content"] = None
            except_result["not"] = True if isinstance(except_result.get("not"), str) and except_result.get(
                "not").upper() == "TRUE" else False
        except Exception as e:
            msg = "前置数据 or 断言类型 or 预期结果json解析失败，请确认格式，{0}".format(e.args)
            return {"is_pass": is_pass, "msg": msg}
        _assert = assert_type.get("type")
        _assert_content = None
        if _assert == "resp.data":
            _assert_content = response.get(assert_type.get("content"))
        elif _assert == "resp.dataArray":
            _assert_content = len(response.get(assert_type.get("content")))
        elif _assert == "resp.code":
            _assert_content = response.get(assert_type.get("content"))
        else:
            msg = "暂不支持的断言类型：{0}".format(_assert)
            return {"is_pass": is_pass, "msg": msg}
        flag = _assert_content == except_result.get("content")
        if except_result.get("not"):
            if flag:
                msg = "真实结果【{0}】取反后与期望结果【{1}】不符合".format(_assert_content, except_result.get("content"))
            else:
                is_pass = "success"
        else:
            if flag:
                is_pass = "success"
            else:
                msg = "真实结果【{0}】与期望结果【{1}】不符合".format(_assert_content, except_result.get("content"))
        return {"is_pass": is_pass, "msg": msg}

    def run_case(self, id):
        case = Case.load_case_by_id(id)
        protocol = case.service.protocol
        host = case.service.host
        port = case.service.port
        if port:
            url = protocol + "://" + host + ":" + port + case.interface.uri
        else:
            url = protocol + "://" + host + case.interface.uri
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
