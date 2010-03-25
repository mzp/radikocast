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
        self.scheduler.add(time=time(12,10),at=time_table.Monday,repeat=True, agent=called('a'))
        self.scheduler.add(time=time(12,10),at=time_table.Monday,repeat=False, agent=called('b'))
        self.scheduler.add(time=time(13,20),at=time_table.Wednesday,repeat=False, agent=called('c'))

    def test_invoke(self):
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 10))
        eq_(1, self.called.get('a',0))
        eq_(1, self.called.get('b',0))
        eq_(0, self.called.get('c',0))

    def test_repeat(self):
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 10))
        self.scheduler.invoke(datetime(2010, 3, 8, 12, 10))
        eq_(2, self.called.get('a',0))

    def test_not_repeat(self):
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 10))
        self.scheduler.invoke(datetime(2010, 3, 8, 12, 10))
        eq_(1, self.called.get('b',0))

    def test_ignore_sec(self):
        self.scheduler.invoke(datetime(2010, 3, 1, 12, 10, 30))
        eq_(1, self.called.get('a',0))
        eq_(1, self.called.get('b',0))
