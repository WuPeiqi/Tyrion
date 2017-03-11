#!/usr/bin/env python
# -*- coding:utf-8 -*-


class FrameworkFactory(object):

    __framework = None

    @staticmethod
    def set_framework(framework):
        FrameworkFactory.__framework = framework

    @staticmethod
    def get_framework():
        return FrameworkFactory.__framework


class BaseFramework(object):
    def get_argument(self, request, name, default=None):
        raise NotImplementedError('class %s must implement get_argument method' % self.__class__)

    def get_arguments(self, request, name, default=None):
        raise NotImplementedError('class %s must implement get_arguments method' % self.__class__)


class Tornado(BaseFramework):
    def get_argument(self, request, name, default=None):
        """
        从请求中获取用户输入或选择的单值
        PS:
            request.get_argument('username',None)        表示从GET和POST等中获取请求
            request.get_query_argument('username',None)  表示从GET中获取请求
            request.get_body_argument('username',None)   表示从POST等中获取请求
        :param request: Tornado请求中的的 xxxHandler对象，即：self；如：self.get_argument('username',None)
        :param name:
        :param default:
        :return:
        """
        return request.get_argument(name, default)

    def get_arguments(self, request, name, default=None):
        """
        从请求中获取用户输入或选择的多个值（列表类型）
        PS:
            request.get_argument('username',None)        表示从GET和POST等中获取请求
            request.get_query_argument('username',None)  表示从GET中获取请求
            request.get_body_argument('username',None)   表示从POST等中获取请求
        :param request: Tornado请求中的的 xxxHandler对象，即：self；如：self.get_argument('username',None)
        :param name:
        :param default:
        :return:
        """
        value = request.get_arguments(name)
        if value:
            return value
        return default


class Django(BaseFramework):
    def get_argument(self, request, name, default=None):
        """
        :param request: Django中request参数
        :param name:
        :param default:
        :return:
        """
        post = request.POST.get(name)
        if post:
            return post
        get = request.GET.get(name)
        if get:
            return get
        return default

    def get_arguments(self, request, name, default=None):
        """

        :param request:
        :param name:
        :param default:
        :return:
        """
        post = request.POST.getlist(name)
        if post:
            return post
        get = request.GET.getlist(name)
        if get:
            return get
        return default


class Flask(BaseFramework):
    def get_argument(self, request, name, default=None):
        """
        从请求中获取用户输入或选择的单值
        PS:
            request.values 表示从GET和POST中获取请求
            request.form  表示从POST中获取请求
            request.arg  表示从GET中获取请求
        :param request: Flask框架中封装了用户请求的request，即：from flask import request
        :param name:
        :param default:
        :return:
        """
        return request.values.get(name, default)

    def get_arguments(self, request, name, default=None):
        """
        从请求中获取用户输入或选择的多个值
        PS:
            request.values 表示从GET和POST中获取请求
            request.form  表示从POST中获取请求
            request.arg  表示从GET中获取请求
        :param request: Flask框架中封装了用户请求的request，即：from flask import request
        :param name:
        :param default:
        :return:
        """
        get_post = request.values.getlist(name)
        if get_post:
            return get_post
        return default


class Bottle(BaseFramework):
    def get_argument(self, request, name, default=None):
        """
        从请求中获取用户输入或选择的单值
        PS:
            request.params 表示从GET和POST中获取请求
            request.forms  表示从POST中获取请求
            request.query  表示从GET中获取请求
        :param request: Bottle框架中封装了用户请求的request，即：from bottle import request
        :param name:
        :param default:
        :return:
        """
        get_post = request.params.get(name, default)
        return get_post

    def get_arguments(self, request, name, default=None):
        """
        从请求中获取用户输入或选择的多个值
        PS:
            request.params 表示从GET和POST中获取请求
            request.forms  表示从POST中获取请求
            request.query  表示从GET中获取请求
        :param request: Bottle框架中封装了用户请求的request，即：from bottle import request
        :param name:
        :param default:
        :return:
        """
        get_post = request.params.getall(name)
        if not get_post:
            return default
        return get_post