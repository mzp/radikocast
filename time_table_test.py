#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-

import unittest
from time_table import *

class TimeTableTest(unittest.TestCase):
    def setUp(self):
        self.program = TimeTable.read("""
- channel: Foo
  time:    12:00
  repeat: Sun
  interval: 0:0:30
- channel: Bar
  time: 13:23
  repeat: Mon
  interval: 30:00
- Bar
  time: 14:00
  repeat: Wed
  interval: 1:0:0
""")

    def time(self, hour,min):
        return (hour * 60 + min) * 60

    def testChannel(self):
        self.assertEqual([ "Foo", "Bar", "Bar" ],
                         [ x.channel for x in self.program ])

    def testTime(self):
        self.assertEqual([ self.time(12,00), self.time(13,23), self.time(14,00) ],
                         [ x.time for x in self.program ])


    def testRepeat(self):
        self.assertEqual([ TimeTable.Sunday, TimeTable.Monday, TimeTable.Wednesday ],
                         [ x.repeat for x in self.program ])

    def testSec(self):
        self.assertEqual([ 30, self.time(0, 30), self.time(1,0) ],
                         [ x.sec for x in self.program ])



if __name__ == '__main__':
    unittest.main()
