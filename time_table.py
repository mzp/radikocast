#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-

import yaml
import re
import open_object
import datetime

def update(dict, key, f):
    dict[key] = f(dict[key])

def parse_time(s):
    (hour,min) = map(int,s.split(":"))
    return datetime.time(hour, min)

def parse_delta(s):
    (hour,min) = map(int,s.split(":"))
    return datetime.timedelta(seconds=((hour*60+min)*60))

( Monday   , Tuesday , Wednesday,
  Thursday , Friday  , Saturday ,
  Sunday   ) = range(7)

RepeatDict = [
    (re.compile("^sun" , re.I), Sunday),
    (re.compile("^mon" , re.I), Monday),
    (re.compile("^tues", re.I), Tuesday),
    (re.compile("^wed" , re.I), Wednesday),
    (re.compile("^thur", re.I), Thursday),
    (re.compile("^fri" , re.I),  Friday),
    (re.compile("^sat" , re.I), Saturday),
]

def parse_repeat(s):
    for (r, v) in RepeatDict:
        if r.match(s):
            return v
    raise StandardError, ("can not parse: %s" % s)


def read(str):
    def parse():
        for x in yaml.load(str):
            update(x, 'time'    , parse_time)
            update(x, 'airtime' , parse_delta)
            update(x, 'at'      , parse_repeat)
            yield open_object.OpenObject(x)
    return TimeTable(parse())

class TimeTable(object):
    def __init__(self, programs):
        self.programs = programs

    def __iter__(self):
        return iter( self.programs )
