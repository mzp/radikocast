#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-

class broadcast(object):
    def __init__(self):
        self.fs = []

    def __iadd__(self, f):
        self.fs.append(f)
        return self

    def __isub__(self, f):
        try:
            self.fs.remove(f)
        except:
            pass
        return self

    def __call__(self, *args, **kargs):
        for f in self.fs:
            print f
            f(*args,**kargs)


