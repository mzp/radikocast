#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-

import unittest
from time_table import *

class TimeTableTest(unittest.TestCase):
    def setUp(self):
        self.program = TimeTable.read(["Foo 12:00 Sun 0:0:30",
                                       "Bar 13:23 Mon 30:00",
                                       "Bar 14:00 Wed 1:0:0"])

    def time(self, hour,min):
        return (hour * 60 + min) * 60

    def testTarget(self):
        self.assertEqual([ "Foo", "Bar", "Bar" ],
                         [ x.target for x in self.program ])

    def testTime(self):
        self.assertEqual([ self.time(12,00), self.time(13,23), self.time(14,00) ],
                         [ x.time for x in self.program ])


    def testWday(self):
        self.assertEqual([ Program.Sunday, Program.Monday, Program.Wednesday ],
                         [ x.wday for x in self.program ])

    def testSec(self):
        self.assertEqual([ 30, self.time(0, 30), self.time(1,0) ],
                         [ x.sec for x in self.program ])



if __name__ == '__main__':
    unittest.main()
