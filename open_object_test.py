#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import unittest
from open_object import *

class OpenObjectTest(unittest.TestCase):
    def setUp(self):
        self.obj = OpenObject({'spam': 'egg', 'answer': 42 })

    def testValue(self):
        self.assertEqual( 'egg', self.obj.spam )
        self.assertEqual( 42   , self.obj.answer )

    def testAssign(self):
        self.obj.answer = 41
        self.assertEqual(41, self.obj.answer)

    def testNewField(self):
        self.obj.foo = 1
        self.assertEqual(1, self.obj.foo)

    def testNotValue(self):
        self.assertEqual(None, self.obj.baz)

if __name__ == '__main__':
    unittest.main()
