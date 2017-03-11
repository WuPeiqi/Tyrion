#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tyrion.Framework import FrameworkFactory
from Tyrion.Framework import Tornado
from Tyrion.Framework import Django
from Tyrion.Framework import Bottle
from Tyrion.Framework import Flask


__version__ = '1.0.1'

def setup(framework='tornado'):
    """
    设置Tyrion插件当前处理的Web框架
    :param framework: Web框架的字符串表示
    :return:
    """
    framework_dict = {
        'tornado': Tornado,
        'django': Django,
        'bottle': Bottle,
        'flask': Flask
    }
    cls = framework_dict.get(framework)
    if cls:
        FrameworkFactory.set_framework(cls())
    else:
        raise Exception('Tyrion模块setup方法参数必须为：%s （任意一种字符串）' % ','.join(framework_dict.keys()))


"""
使用方法：导入模块并且设置使得其支持不同的Web框架

如：
    import Tyrion
    Tyrion.setup('tornado')

"""

