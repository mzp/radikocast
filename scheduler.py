#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
from datetime import *
from itertools import *
import calendar

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def imerge(x, y):
    i = iter(x)
    j = iter(y)


class Scheduler(object):
    def __init__(self):
        self.table = iter([])

    def now(self):
        return datetime.today()

    def add(self, time, at, repeat, airtime, callback):
        now   = self.now()
        def stream():
            date = now.date()
            while True:
                yield datetime.combine(date, time)
                date = date + timedelta(days=1)
        days = stream()
        if at != None:
            days = ifilter(lambda t: t.date().weekday() == at, days)
        if repeat == False:
            days = take(1, days)
        self.table = imerge(days, self.table)
        take(1, self.table)

    def invoke(self,datetime):
        pass

    def match(self, datetime, program):
        pass
