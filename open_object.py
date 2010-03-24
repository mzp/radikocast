#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-

class OpenObject(object):
    def __init__(self, hash = {}):
        self.__dict__.update(hash)

    def __getattr__(self, name):
        return None

