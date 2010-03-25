#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import unittest
import datetime
from time_table import *

class TimeTableTest(unittest.TestCase):
    def setUp(self):
        self.program = read("""
- channel: Foo
  time:    "12:00"
  repeat: true
  at: Sun
  interval: "0:30"
  foo : bar
- channel: Bar
  time: "13:23"
  repeat: false
  at: Monday
  interval: "00:30"
- channel: Bar
  time: "14:00"
  repeat: true
  at: Wed
  interval: "1:00"
""")

    def time(self, hour,min):
        return datetime.time(hour,min)

    def testChannel(self):
        self.assertEqual([ "Foo", "Bar", "Bar" ],
                         [ x.channel for x in self.program ])

    def testTime(self):
        self.assertEqual([ self.time(12,00), self.time(13,23), self.time(14,00) ],
                         [ x.time for x in self.program ])


    def testAt(self):
        self.assertEqual([ Sunday, Monday, Wednesday ],
                         [ x.at for x in self.program ])

    def testSec(self):
        self.assertEqual([ self.time(0,30), self.time(0, 30), self.time(1,0) ],
                         [ x.interval for x in self.program ])

    def testOther(self):
        self.assertEqual(['bar',None,None],
                         [x.foo for x in self.program])

    def testRepeat(self):
        self.assertEqual([True, False, True],
                         [x.repeat for x in self.program])


