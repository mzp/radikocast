#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
from datetime import *

class Scheduler(object):
    def __init__(self):
        self.table = []

    def now(self):
        return datetime.today()

    def add(self, time, at, repeat, airtime, callback):
        now = self.now()
        if now.time() <= time < now.time() + airtime:
            start = now
        else:

    def invoke(self,datetime):
        pass

    def match(self, datetime, program):
        pass
