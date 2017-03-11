#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Input(object):
    def __init__(self, attr=None):
        """
        :param attr: 生成的HTML属性，如：{'id': '123'}
        :return:
        """
        self.attr = attr if attr else {}

    def __str__(self):
        """
        使用对象时返回的字符串
        :return:
        """
        t = "<input %s />"
        attr_list = []
        for k, v in self.attr.items():
            temp = "%s='%s' " % (k, v,)
            attr_list.append(temp)
        tag = t % (''.join(attr_list))
        return tag


class InputText(Input):
    def __init__(self, attr=None):
        attr_dict = {'type': 'text'}
        if attr:
            attr_dict.update(attr)
        super(InputText, self).__init__(attr_dict)


class InputEmail(Input):
    def __init__(self, attr=None):
        attr_dict = {'type': 'email'}
        if attr:
            attr_dict.update(attr)
        super(InputEmail, self).__init__(attr_dict)


class InputPassword(Input):
    def __init__(self, attr=None):
        attr_dict = {'type': 'password'}
        if attr:
            attr_dict.update(attr)
        super(InputPassword, self).__init__(attr_dict)


class InputSingleCheckBox(Input):
    def __init__(self, attr=None):
        attr_dict = {'type': 'checkbox'}
        if attr:
            attr_dict.update(attr)
        super(InputSingleCheckBox, self).__init__(attr_dict)

    def __str__(self):
        """
        使用对象时返回的字符串
        :return:
        """
        t = "<input %s />"
        attr_list = []
        for k, v in self.attr.items():
            temp = "%s='%s' " % (k, v,)
            attr_list.append(temp)
        tag = t % (''.join(attr_list))
        return tag


class InputMultiCheckBox(object):
    def __init__(self, attr=None, text_value_list=None, checked_value_list=None):
        """
        :param attr: 生成的HTML属性，如：{'id': '123'}
        :param text_value_list: 生成CheckBox的value和内容，如：
                                [
                                    {'value':1, 'text': '篮球'},
                                    {'value':2, 'text': '足球'},
                                    {'value':3, 'text': '乒乓球'},
                                    {'value':4, 'text': '羽毛球'},
                                ]
        :param checked_value_list: 被选中的checked_value_list，如：[2,3]
        :return:
        """
        attr_dict = {'type': 'checkbox'}
        if attr:
            attr_dict.update(attr)
        self.attr = attr_dict

        self.text_value_list = text_value_list if text_value_list else []
        self.checked_value_list = checked_value_list if checked_value_list else []

    def __str__(self):
        """
        使用对象时返回的字符串
        :return:
        """
        tag_list = []
        for item in self.text_value_list:
            a = "<div><span>%s</span><span>%s</span></div>"
            b = "<input %s />"
            attr_list = []
            for k, v in self.attr.items():
                temp = "%s='%s' " % (k, v,)
                attr_list.append(temp)
            attr_list.append("%s='%s' " % ('value', item['value']))
            if item['value'] in self.checked_value_list:
                attr_list.append("checked='checked' ")
            input_tag = b % (''.join(attr_list))
            c = a % (input_tag, item['text'], )
            tag_list.append(c)
        return ''.join(tag_list)


class InputRadio(object):
    def __init__(self, attr=None, text_value_list=None, checked_value=None):
        """
        :param attr: 生成的HTML属性，如：{'id': '123'}
        :param text_value_list: 生成radio的value和内容，如：
                                [
                                    {'value':1, 'text': '篮球'},
                                    {'value':2, 'text': '足球'},
                                    {'value':3, 'text': '乒乓球'},
                                    {'value':4, 'text': '羽毛球'},
                                ]
        :param checked_value: 被选中的checked_value，如：2
        :return:
        """
        attr_dict = {'type': 'radio'}
        if attr:
            attr_dict.update(attr)
        self.attr = attr_dict

        self.text_value_list = text_value_list if text_value_list else []
        self.checked_value = checked_value

    def __str__(self):
        """
        使用对象时返回的字符串
        :return:
        """
        tag_list = []
        for item in self.text_value_list:
            a = "<div><span>%s</span><span>%s</span></div>"
            b = "<input %s />"
            attr_list = []
            for k, v in self.attr.items():
                temp = "%s='%s' " % (k, v,)
                attr_list.append(temp)
            attr_list.append("%s='%s' " % ('value', item['value']))
            if item['value'] == self.checked_value:
                attr_list.append("checked='checked' ")
            input_tag = b % (''.join(attr_list))
            c = a % (input_tag,item['text'])
            tag_list.append(c)
        return ''.join(tag_list)


class SingleSelect(object):
    def __init__(self, attr=None, text_value_list=None, selected_value=None):
        """
        :param attr: 生成的HTML属性，如：{'id': '123'}
        :param text_value_list: 生成select的value和内容，如：
                                [
                                    {'value':1, 'text': '篮球'},
                                    {'value':2, 'text': '足球'},
                                    {'value':3, 'text': '乒乓球'},
                                    {'value':4, 'text': '羽毛球'},
                                ]
        :param selected_value: 被选中的checked_value，如：2
        :return:
        """
        attr_dict = {}
        if attr:
            attr_dict.update(attr)
        self.attr = attr_dict

        self.text_value_list = text_value_list if text_value_list else []
        self.selected_value = selected_value

    def __str__(self):
        """
        使用对象时返回的字符串
        :return:
        """

        a = "<select %s>%s</select>"

        attr_list = []
        for k, v in self.attr.items():
            temp = "%s='%s' " % (k, v,)
            attr_list.append(temp)

        option_list = []

        for item in self.text_value_list:

            if item['value'] == self.selected_value:
                b = "<option selected='selected' value='%s'>%s</option>"
            else:
                b = "<option value='%s'>%s</option>"
            option = b % (item['value'], item['text'],)
            option_list.append(option)

        tag = a % (''.join(attr_list), ''.join(option_list))

        return tag


class MultiSelect(object):
    def __init__(self, attr=None, text_value_list=None, selected_value_list=None):
        """
        :param attr: 生成的Select标签的属性，如：{'id': '123'}
        :param text_value_list: 生成CheckBox的value和内容，如：
                                [
                                    {'value':1, 'text': '篮球'},
                                    {'value':2, 'text': '足球'},
                                    {'value':3, 'text': '乒乓球'},
                                    {'value':4, 'text': '羽毛球'},
                                ]
        :param selected_value_list: selected_value_list，如：[2,3,4]
        :return:
        """
        attr_dict = {'multiple': 'multiple'}
        if attr:
            attr_dict.update(attr)
        self.attr = attr_dict

        self.text_value_list = text_value_list if text_value_list else []
        self.selected_value_list = selected_value_list if selected_value_list else []

    def __str__(self):
        """
        使用对象时返回的字符串
        :return:
        """

        a = "<select %s>%s</select>"

        attr_list = []
        for k, v in self.attr.items():
            temp = "%s='%s' " % (k, v,)
            attr_list.append(temp)

        option_list = []
        for item in self.text_value_list:
            if item['value'] in self.selected_value_list:
                b = "<option selected='selected' value='%s'>%s</option>"
            else:
                b = "<option value='%s'>%s</option>"
            option = b % (item['value'], item['text'],)
            option_list.append(option)

        tag = a % (''.join(attr_list), ''.join(option_list))
        return tag


class TextArea(object):
    def __init__(self, attr=None, value=""):
        """
        :param attr: 生成的HTML属性，如：{'id': '123'}
        :return:
        """
        self.attr = attr if attr else {}
        self.value = value

    def __str__(self):
        """
        使用对象时返回的字符串
        :return:
        """
        t = "<textarea %s>%s</textarea>"
        attr_list = []
        for k, v in self.attr.items():
            temp = "%s='%s' " % (k, v,)
            attr_list.append(temp)
        tag = t % (''.join(attr_list), self.value)
        return tag

