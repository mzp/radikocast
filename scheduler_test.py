#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import time_table
from datetime import *
from scheduler import *
from nose.tools import *

class TestScheduler:
    def setUp(self):
        def called(name):
            def f(): self.called[name] = self.called.get(name,0) + 1
            return f
        self.called = {}
        self.scheduler = Scheduler()
        self.scheduler.add(time     = time(12,10),
                           at       = time_table.Monday,
                           airtime  = timedelta(seconds=600),
                           repeat   = True,
                           callback = called('a'),
                           now      = datetime(2010,3,1,12,00))
        self.scheduler.add(time     = time(12,10),
                           at       = time_table.Monday,
                           airtime  = timedelta(seconds=600),
                           repeat   = False,
                           callback = called('b'),
                           now      = datetime(2010,3,1,12,00))
        self.scheduler.add(time     = time(13,20),
                           at       = time_table.Wednesday,
                           airtime  = timedelta(seconds=600),
                           repeat   = False,
                           callback = called('c'),
                           now      = datetime(2010,3,1,12,00))

    def  count(self, name):
        return self.called.get(name,0)

    def test_invoke(self):
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 10))
        eq_(1, self.count('a'))
        eq_(1, self.count('b'))
        eq_(0, self.count('c'))

    def test_repeat(self):
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 10))
        self.scheduler.invoke(datetime(2010, 3, 8, 12, 10))
        eq_(2, self.count('a'))

    def test_not_repeat(self):
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 10))
        self.scheduler.invoke(datetime(2010, 3, 8, 12, 10))
        eq_(1, self.count('b'))

    def test_ignore_sec(self):
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 10, 30))
        eq_(1, self.count('a'))
        eq_(1, self.count('b'))

    def test_not_invoke_duplicate(self):
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 10))
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 11))
        eq_(1, self.count('a'))
        eq_(1, self.count('b'))
        eq_(0, self.count('c'))

    def test_invoke_later(self):
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 11))
        eq_(1, self.count('a'))
        eq_(1, self.count('b'))
        eq_(0, self.count('c'))

    def test_not_invoke_later(self):
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 21))
        eq_(0, self.count('a'))
        eq_(0, self.count('b'))
        eq_(0, self.count('c'))
