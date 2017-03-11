#!/usr/bin/env python
# -*- coding:utf-8 -*-
import copy
from Tyrion.Fields import Field


class Form(object):
    def __init__(self, handler=None):
        """

        :param handler: Tornado请求中的XXXHandler对象
        :return:
        """
        self.handler = handler
        self.FiledDict = {}
        self.value_dict = {}
        self.error_dict = {}
        self.valid_status = True

        self.initialize()

    def initialize(self):
        """
        初始化，将派生类Form中的静态字段拷贝到字段FiledDict中，并为字段对应的Html插件设置id和name属性
        :return:
        """
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Field):
                field = copy.deepcopy(v)
                field.name = k
                field.widget.attr['name'] = k
                """
                if 'id' not in field.widget.attr:
                    field.widget.attr['id'] = '%s_%s' % ('id', k)
                """
                self.FiledDict[k] = field
        self.__dict__.update(self.FiledDict)

    def is_valid(self):
        """
        验证用户输入和规则是否匹配
        :return:
        """
        for k, v in self.FiledDict.items():
            v.valid(self.handler)
            if v.status:
                self.value_dict[k] = v.value
            else:
                self.error_dict[k] = v.error
                self.valid_status = False

        return self.valid_status

    def init_field_value(self, value_dict):
        """
        设置默认 显示的值 或 选中的值
        :param value_dict:
        :return:
        """
        for k, v in self.FiledDict.items():
            v.set_value(value_dict.get(k, None))

