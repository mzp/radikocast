#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import broadcast
from nose.tools import *

class TestStorage:
    def setUp(self):
        def f(*xs,**ys):
            self.called = (xs,ys)

        self.broadcast = broadcast.broadcast()
        self.broadcast += f

    def test_call_with_args(self):
        self.broadcast(42)
        eq_(((42,), {}), self.called)

        self.broadcast(x=1)
        eq_(((), {'x' : 1}), self.called)


        self.broadcast(42,x=1)
        eq_(((42,), {'x' : 1}), self.called)

    def test_add(self):
        self.callp = False
        def f():
            self.callp = True
        self.broadcast += f
        self.broadcast()
        eq_(True, self.callp)

    def test_sub(self):
        self.callp = False
        def f():
            self.callp = True
        self.broadcast += f
        self.broadcast -= f
        self.broadcast()
        eq_(False, self.callp)

    def test_sub_safe(self):
        def f():
            pass
        self.broadcast -= f

