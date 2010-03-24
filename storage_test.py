#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-

from storage import *
from nose.tools import *
import os
class TestStorage:
    def setUp(self):
        try:
            os.remove('test.db')
        except:
            pass

        self.storage = Storage('test.db')
        self.p1 = { 'name' : "program1",
                    'created_at' : 1,
                    'path' : "1.aac" }
        self.p2 = { 'name' : "program1",
                    'created_at' : 2,
                    'path' : "2.aac" }
        self.p3 = { 'name' : "program2",
                    'created_at' : 1,
                    'path' : "3.aac" }
        self.storage.add(**self.p1)
        self.storage.add(**self.p2)
        self.storage.add(**self.p3)

    def tearDown(self):
        os.remove('test.db')

    def test_fisd_by_path(self):
        program = self.storage.find_by_path("3.aac")
        eq_(self.p3, program)

        program = self.storage.find_by_path("????")
        eq_(None, program)

    def test_find_by_name(self):
        programs = self.storage.find_by_name("program1")
        eq_([ self.p2, self.p1 ], programs)

    def test_find_all(self):
        programs = self.storage.find_all()
        expect = [
            ("program1", [self.p2, self.p1] ),
            ("program2", [self.p3 ])
            ]
        eq_(expect, programs)
