#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
from datetime import *
from itertools import *
import calendar

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def imerge(xs, ys, p):
    xs = iter(xs)
    ys = iter(ys)
    try:
        x = None
        y = None
        while True:
            if x == None: x = xs.next()
            if y == None: y = ys.next()
            if p(x,y):
                yield x
                x = None
            else:
                yield y
                y = None
    except StopIteration:
        if x != None: yield x
        if y != None: yield y
        for x in xs:
            yield x
        for y in ys:
            yield y
        raise StopIteration

class Scheduler(object):
    def __init__(self):
        self.table = iter([])

    def add(self, time, airtime, callback, repeat=None, at=None, now=datetime.now()):
        def stream():
            date = now.date()
            while True:
                yield datetime.combine(date, time)
                date = date + timedelta(days=1)
        days = dropwhile(lambda t: t + airtime < now, stream())
        if at != None:
            days = ifilter(lambda t: t.date().weekday() == at, days)
        if not repeat:
            days = take(1, days)
        self.table = imerge(imap(lambda t: { 'time' : t,
                                             'airtime' : airtime,
                                             'callback' : callback },
                                 days),
                            self.table,
                            lambda x,y: x['time'] < y['time'])

    def invoke(self, now):
        for x in takewhile(lambda t: t['time'] <= now, self.table):
            if now <= x['time'] + x['airtime']:
                x['callback'](now, (x['time'] + x['airtime']) - now)

