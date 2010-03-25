#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import unittest
from datetime import *
from time_table import *

class TimeTableTest(unittest.TestCase):
    def setUp(self):
        self.program = read("""
- channel: Foo
  time:    "12:00"
  repeat: true
  at: Sun
  airtime: "0:30"
  foo : bar
- channel: Bar
  time: "13:23"
  repeat: false
  at: Monday
  airtime: "00:30"
- channel: Bar
  time: "14:00"
  repeat: true
  at: Wed
  airtime: "1:00"
""")

    def testChannel(self):
        self.assertEqual([ "Foo", "Bar", "Bar" ],
                         [ x.channel for x in self.program ])

    def testTime(self):
        self.assertEqual([ time(12,00), time(13,23), time(14,00) ],
                         [ x.time for x in self.program ])


    def testAt(self):
        self.assertEqual([ Sunday, Monday, Wednesday ],
                         [ x.at for x in self.program ])

    def testSec(self):
        self.assertEqual([ timedelta(seconds=60*30), timedelta(seconds=60*30), timedelta(seconds=60*60) ],
                         [ x.airtime for x in self.program ])

    def testOther(self):
        self.assertEqual(['bar',None,None],
                         [x.foo for x in self.program])

    def testRepeat(self):
        self.assertEqual([True, False, True],
                         [x.repeat for x in self.program])


