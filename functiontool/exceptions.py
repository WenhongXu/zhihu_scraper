# -*- coding: utf-8 -*-
# @Author: Vincent Xu
# @E-mail: wenhong0815@qq.com
# For my Graduation Design about RS

# exceptions



class ReadOnlyError(Exception):
    '''
    when trying to modify a readonly object
    '''
    pass


class WriteOnlyError(Exception):
    '''
    when trying to modify a writeonly object
    '''
    pass


class PropertyError(Exception):
    '''
    lack necessary property while create database instance
    '''
    pass

class ErrorInJson(Exception):
    pass

class WrongStatuCode(Exception):
    pass

class NoSuchLiveTag(Exception):
    pass

class NoMoreLine(Exception):
    pass

class BloomError(Exception):
    pass

class BadTemp(Exception):
    pass