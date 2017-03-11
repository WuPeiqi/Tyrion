#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from Tyrion import Widget
from Tyrion.Framework import FrameworkFactory


class Field(object):
    """
    所有Form字段的基类
    """

    def __init__(self, widget):
        self.status = False
        self.name = None
        self.value = None
        self.error = None
        self.widget = widget

    def valid(self, handler):
        """
        字段必须实现该方法，用于从请求中获取用户输入的值并和规则进行比较
        :param handler: Tornado处理请求的XXXHandler对象
        :return:
        """
        raise NotImplementedError('your class %s must implement valid method' % self.__class__)

    def __str__(self):

        if self.value == None:
            return str(self.widget)

        if isinstance(self.widget, Widget.SingleSelect):
            self.widget.selected_value = self.value
        elif isinstance(self.widget, Widget.MultiSelect):
            self.widget.selected_value_list = self.value
        elif isinstance(self.widget, Widget.InputSingleCheckBox):
            self.widget.attr['checked'] = 'checked'
        elif isinstance(self.widget, Widget.InputMultiCheckBox):
            self.widget.checked_value_list = self.value
        elif isinstance(self.widget, Widget.InputRadio):
            self.widget.checked_value = self.value
        elif isinstance(self.widget, Widget.TextArea):
            self.widget.value = self.value
        else:
            self.widget.attr['value'] = self.value
        return str(self.widget)

    def set_value(self, value):
        self.value = value


class StringField(Field):
    """
    字符串类字段
    """
    REGULAR = "^.*$"
    DEFAULT_WIDGET = Widget.InputText

    def __init__(self, max_length=None, min_length=None, error=None, required=True, widget=None):
        """
        :param error: 自定义错误信息
                      如：{
                            'required': '值为空时的错误提示',
                            'invalid': '格式错误时的错误提示',
                            'max_length': '最大长度为10',
                            'min_length': '最小长度为1',
                         }
        :param required: 是否必须
        :param widget: 指定插件，用于生成HTML标签（默认生成Input标签）
        :return:
        """
        self.custom_error_dict = {}
        if error:
            self.custom_error_dict.update(error)

        self.required = required
        self.max_length = max_length
        self.min_length = min_length

        widget = widget if widget else self.DEFAULT_WIDGET()

        super(StringField, self).__init__(widget)

    def valid(self, handler):
        """
        从请求中获取用户输入的值并和规则进行比较
        :param handler: Tornado处理请求的XXXHandler对象
        :return:
        """
        input_value = FrameworkFactory.get_framework().get_argument(handler, self.name, None)
        # input_value = handler.get_argument(self.name, None)

        self.value = input_value

        if not input_value:
            if not self.required:
                self.status = True
                return

            if self.custom_error_dict.get('required', None):
                self.error = self.custom_error_dict['required']
            else:
                self.error = "%s is required" % self.name
            return

        ret = re.match(self.REGULAR, input_value)
        if not ret:
            if self.custom_error_dict.get('invalid', None):
                self.error = self.custom_error_dict['invalid']
            else:
                self.error = "%s is invalid" % self.name
            return

        if self.max_length:
            if len(input_value) > self.max_length:
                if self.custom_error_dict.get('max_length', None):
                    self.error = self.custom_error_dict['max_length']
                else:
                    self.error = "%s max length is %s" % (self.name, self.max_length)
                return

        if self.min_length:

            if len(input_value) < self.min_length:
                if self.custom_error_dict.get('min_length', None):
                    self.error = self.custom_error_dict['min_length']
                else:
                    self.error = "%s min length is %s" % (self.name, self.min_length)
                return

        self.status = True


class EmailField(Field):
    """
    字符串类字段
    """
    REGULAR = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
    DEFAULT_WIDGET = Widget.InputText

    def __init__(self, max_length=None, min_length=None, error=None, required=True, widget=None):
        """
        :param error: 自定义错误信息
                      如：{
                            'required': '值为空时的错误提示',
                            'invalid': '格式错误时的错误提示',
                            'max_length': '最大长度为10',
                            'min_length': '最小长度为1',
                         }
        :param required: 是否必须
        :param widget: 指定插件，用于生成HTML标签（默认生成Input标签）
        :return:
        """
        self.custom_error_dict = {}
        if error:
            self.custom_error_dict.update(error)

        self.required = required
        self.max_length = max_length
        self.min_length = min_length

        widget = widget if widget else self.DEFAULT_WIDGET()

        super(EmailField, self).__init__(widget)

    def valid(self, handler):
        """
        从请求中获取用户输入的值并和规则进行比较
        :param handler: Tornado处理请求的XXXHandler对象
        :return:
        """

        input_value = FrameworkFactory.get_framework().get_argument(handler, self.name, None)
        # input_value = handler.get_argument(self.name, None)

        self.value = input_value
        if not input_value:
            if not self.required:
                self.status = True
                return
            if self.custom_error_dict.get('required', None):
                self.error = self.custom_error_dict['required']
            else:
                self.error = "%s is required" % self.name
            return

        ret = re.match(self.REGULAR, input_value)
        if not ret:
            if self.custom_error_dict.get('invalid', None):
                self.error = self.custom_error_dict['invalid']
            else:
                self.error = "%s is invalid" % self.name
            return

        if self.max_length:
            if len(input_value) > self.max_length:
                if self.custom_error_dict.get('max_length', None):
                    self.error = self.custom_error_dict['max_length']
                else:
                    self.error = "%s max length is %s" % (self.name, self.max_length)
                return

        if self.min_length:
            if len(input_value) < self.max_length:
                if self.custom_error_dict.get('min_length', None):
                    self.error = self.custom_error_dict['min_length']
                else:
                    self.error = "%s min length is %s" % (self.name, self.min_length)
                return

        self.status = True


class IPField(Field):
    """
    字符串类字段
    """
    REGULAR = "^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$"
    DEFAULT_WIDGET = Widget.InputText

    def __init__(self, max_length=None, min_length=None, error=None, required=True, widget=None):
        """
        :param error: 自定义错误信息
                      如：{
                            'required': '值为空时的错误提示',
                            'invalid': '格式错误时的错误提示',
                            'max_length': '最大长度为10',
                            'min_length': '最小长度为1',
                         }
        :param required: 是否必须
        :param widget: 指定插件，用于生成HTML标签（默认生成Input标签）
        :return:
        """
        self.custom_error_dict = {}
        if error:
            self.custom_error_dict.update(error)

        self.required = required
        self.max_length = max_length
        self.min_length = min_length

        widget = widget if widget else self.DEFAULT_WIDGET()

        super(IPField, self).__init__(widget)

    def valid(self, handler):
        """
        从请求中获取用户输入的值并和规则进行比较
        :param handler: Tornado处理请求的XXXHandler对象
        :return:
        """
        input_value = FrameworkFactory.get_framework().get_argument(handler, self.name, None)
        # input_value = handler.get_argument(self.name, None)

        self.value = input_value
        if not input_value:
            if not self.required:
                self.status = True
                return

            if self.custom_error_dict.get('required', None):
                self.error = self.custom_error_dict['required']
            else:
                self.error = "%s is required" % self.name
            return

        ret = re.match(self.REGULAR, input_value)
        if not ret:
            if self.custom_error_dict.get('invalid', None):
                self.error = self.custom_error_dict['invalid']
            else:
                self.error = "%s is invalid" % self.name
            return

        if self.max_length:
            if len(input_value) > self.max_length:
                if self.custom_error_dict.get('max_length', None):
                    self.error = self.custom_error_dict['max_length']
                else:
                    self.error = "%s max length is %s" % (self.name, self.max_length)
                return

        if self.min_length:
            if len(input_value) < self.max_length:
                if self.custom_error_dict.get('min_length', None):
                    self.error = self.custom_error_dict['min_length']
                else:
                    self.error = "%s min length is %s" % (self.name, self.min_length)
                return

        self.status = True


class IntegerField(Field):
    """
    字符串类字段
    """
    REGULAR = "^\d+$"
    DEFAULT_WIDGET = Widget.InputText

    def __init__(self, max_value=None, min_value=None, error=None, required=True, widget=None):
        """
        :param error: 自定义错误信息
                      如：{
                            'required': '值为空时的错误提示',
                            'invalid': '格式错误时的错误提示',
                            'max_value': '最大值为10',
                            'max_value': '最小值度为1',
                         }
        :param required: 是否必须
        :param widget: 指定插件，用于生成HTML标签（默认生成Input标签）
        :return:
        """
        self.custom_error_dict = {}
        if error:
            self.custom_error_dict.update(error)

        self.required = required
        self.max_value = max_value
        self.min_value = min_value

        widget = widget if widget else self.DEFAULT_WIDGET()

        super(IntegerField, self).__init__(widget)

    def valid(self, handler):
        """
        从请求中获取用户输入的值并和规则进行比较
        :param handler: Tornado处理请求的XXXHandler对象
        :return:
        """
        input_value = FrameworkFactory.get_framework().get_argument(handler, self.name, None)
        # input_value = handler.get_argument(self.name, None)

        self.value = input_value

        if not input_value:
            if not self.required:
                self.status = True
                return

            if self.custom_error_dict.get('required', None):
                self.error = self.custom_error_dict['required']
            else:
                self.error = "%s is required" % self.name
            return

        ret = re.match(self.REGULAR, input_value)
        if not ret:
            if self.custom_error_dict.get('invalid', None):
                self.error = self.custom_error_dict['invalid']
            else:
                self.error = "%s is invalid" % self.name
            return

        input_value = int(input_value)
        self.value = input_value

        if self.max_value:
            if input_value > self.max_value:
                if self.custom_error_dict.get('max_value', None):
                    self.error = self.custom_error_dict['max_value']
                else:
                    self.error = "%s max value is %s" % (self.name, self.max_value)
                return

        if self.min_value:
            if input_value < self.min_value:
                if self.custom_error_dict.get('min_value', None):
                    self.error = self.custom_error_dict['min_value']
                else:
                    self.error = "%s min value is %s" % (self.name, self.min_value)
                return

        self.status = True


class FloatField(Field):
    """
    字符串类字段
    """
    REGULAR = "^\d+(\.\d{1,2})?$"
    DEFAULT_WIDGET = Widget.InputText

    def __init__(self, max_value=None, min_value=None, error=None, required=True, widget=None):
        """
        :param error: 自定义错误信息
                      如：{
                            'required': '值为空时的错误提示',
                            'invalid': '格式错误时的错误提示',
                            'max_value': '最大值为10',
                            'min_value': '最小值度为1',
                         }
        :param required: 是否必须
        :param widget: 指定插件，用于生成HTML标签（默认生成Input标签）
        :return:
        """
        self.custom_error_dict = {}
        if error:
            self.custom_error_dict.update(error)

        self.required = required
        self.max_value = max_value
        self.min_value = min_value

        widget = widget if widget else self.DEFAULT_WIDGET()

        super(FloatField, self).__init__(widget)

    def valid(self, handler):
        """
        从请求中获取用户输入的值并和规则进行比较
        :param handler: Tornado处理请求的XXXHandler对象
        :return:
        """
        input_value = FrameworkFactory.get_framework().get_argument(handler, self.name, None)
        # input_value = handler.get_argument(self.name, None)

        self.value = input_value
        if not input_value:
            if not self.required:
                self.status = True
                return

            if self.custom_error_dict.get('required', None):
                self.error = self.custom_error_dict['required']
            else:
                self.error = "%s is required" % self.name
            return

        ret = re.match(self.REGULAR, input_value)
        if not ret:
            if self.custom_error_dict.get('invalid', None):
                self.error = self.custom_error_dict['invalid']
            else:
                self.error = "%s is invalid" % self.name
            return

        input_value = float(input_value)
        self.value = input_value

        if self.max_value:
            if input_value > self.max_value:
                if self.custom_error_dict.get('max_value', None):
                    self.error = self.custom_error_dict['max_value']
                else:
                    self.error = "%s max value is %s" % (self.name, self.max_value)
                return

        if self.min_value:
            if input_value < self.min_value:
                if self.custom_error_dict.get('min_value', None):
                    self.error = self.custom_error_dict['min_value']
                else:
                    self.error = "%s min value is %s" % (self.name, self.min_value)
                return

        self.status = True


class StringListField(Field):
    """
    字符串类字段
    """
    REGULAR = "^.*$"
    DEFAULT_WIDGET = Widget.InputMultiCheckBox

    def __init__(self, ele_max_length=None, ele_min_length=None, error=None, required=True, widget=None):
        """
        :param error: 自定义错误信息
                      如：{
                            'required': '值为空时的错误提示',
                            'element': '列表中的元素必须是字符串',
                            'ele_max_length': '最大长度为10',
                            'ele_min_length': '最小长度为1',
                         }
        :param required: 是否必须
        :param widget: 指定插件，用于生成HTML标签（默认生成Input标签）
        :return:
        """
        self.custom_error_dict = {}
        if error:
            self.custom_error_dict.update(error)

        self.required = required
        self.ele_max_length = ele_max_length
        self.ele_min_length = ele_min_length

        widget = widget if widget else self.DEFAULT_WIDGET()

        super(StringListField, self).__init__(widget)

    def valid(self, handler):
        """
        从请求中获取用户输入的值并和规则进行比较
        :param handler: Tornado处理请求的XXXHandler对象
        :return:
        """
        input_value = FrameworkFactory.get_framework().get_arguments(handler, self.name, [])
        # input_value = handler.get_arguments(self.name)

        self.value = input_value

        if not input_value:
            if not self.required:
                self.status = True
                return

            if self.custom_error_dict.get('required', None):
                self.error = self.custom_error_dict['required']
            else:
                self.error = "%s is required" % self.name
            return

        for value in input_value:
            ret = re.match(self.REGULAR, value)
            if not ret:
                if self.custom_error_dict.get('element', None):
                    self.error = self.custom_error_dict['element']
                else:
                    self.error = "element %s is invalid" % self.name
                return

            if self.ele_max_length:
                if len(value) > self.ele_max_length:
                    if self.custom_error_dict.get('ele_max_length', None):
                        self.error = self.custom_error_dict['ele_max_length']
                    else:
                        self.error = "element %s max length is %s" % (self.name, self.ele_max_length)
                    return

            if self.ele_min_length:

                if len(value) < self.ele_min_length:
                    if self.custom_error_dict.get('ele_min_length', None):
                        self.error = self.custom_error_dict['ele_min_length']
                    else:
                        self.error = "element %s min length is %s" % (self.name, self.ele_min_length)
                    return

        self.status = True


class IntegerListField(Field):
    """
    字符串类字段
    """
    REGULAR = "^\d+$"
    DEFAULT_WIDGET = Widget.InputMultiCheckBox

    def __init__(self, ele_max_value=None, ele_min_value=None, error=None, required=True, widget=None):
        """
        :param error: 自定义错误信息
                      如：{
                            'required': '值为空时的错误提示',
                            'element': '列表中的元素必须是数字',
                            'ele_max_value': '最大值为x',
                            'ele_min_value': '最小值为x',
                         }
        :param required: 是否必须
        :param widget: 指定插件，用于生成HTML标签（默认生成Input标签）
        :return:
        """
        self.custom_error_dict = {}
        if error:
            self.custom_error_dict.update(error)

        self.required = required
        self.ele_max_value = ele_max_value
        self.ele_min_value = ele_min_value

        widget = widget if widget else self.DEFAULT_WIDGET()

        super(IntegerListField, self).__init__(widget)

    def valid(self, handler):
        """
        从请求中获取用户输入的值并和规则进行比较
        :param handler: Tornado处理请求的XXXHandler对象
        :return:
        """
        input_value = FrameworkFactory.get_framework().get_arguments(handler, self.name, [])
        # input_value = handler.get_arguments(self.name)
        self.value = input_value

        if not input_value:
            if not self.required:
                self.status = True
                return

            if self.custom_error_dict.get('required', None):
                self.error = self.custom_error_dict['required']
            else:
                self.error = "%s is required" % self.name
            return

        success_value_list = []
        for value in input_value:
            ret = re.match(self.REGULAR, value)
            if not ret:
                if self.custom_error_dict.get('element', None):
                    self.error = self.custom_error_dict['element']
                else:
                    self.error = "element %s is invalid" % self.name
                return
            value = int(value)
            success_value_list.append(value)

            if self.ele_max_value:
                if value > self.ele_max_value:
                    if self.custom_error_dict.get('ele_max_value', None):
                        self.error = self.custom_error_dict['ele_max_value']
                    else:
                        self.error = "element %s max value is %s" % (self.name, self.ele_max_value)
                    return

            if self.ele_min_value:

                if value < self.ele_min_value:
                    if self.custom_error_dict.get('ele_min_value', None):
                        self.error = self.custom_error_dict['ele_min_value']
                    else:
                        self.error = "element %s min value is %s" % (self.name, self.ele_min_value)
                    return

        self.value = success_value_list
        self.status = True