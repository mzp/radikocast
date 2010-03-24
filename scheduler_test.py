#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-


from scheduler import *
import time_table
def time(hour,min):
    return (hour * 60 + min) * 60

class TestScheduler:
    def setUp(self):
        def called(name):
            def f(): self.called[name] = True
            return f
        self.called = {}
        self.scheduler = Scheduler()
        self.scheduler.add(time=time(12,10),at=time_table.Monday, agent=called('a'))
        self.scheduler.add(time=time(13,20),at=time_table.Wednesday, agent=called('b'))
        self.scheduler.add(time=time(12,10),at=time_table.Single, agent=called('c'))

    def test_invoke(self):
        assert 1 == 1

    def test_repeat(self):
        pass

    def test_not_repeat(self):
        pass

    def test_ignore_sec(self):
        pass
