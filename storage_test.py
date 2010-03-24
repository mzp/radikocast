#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-

from storage import *

class TestStorage:
    def setUp(self):
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


    def test_fisd_by_path(self):
        program = self.storage.find_by_path("3.aac")
        assert self.p3 == program

    def test_find_by_name(self):
        programs = self.storage.find_by_path("program1")
        assert [ self.p2, self.p1 ] == programs

    def test_find_all(self):
        programs = self.storage.find_all()
        expect = [
            ("program1", [self.p2, self.p1] ),
            ("program2", [self.p3 ])
            ]
        assert expect == programs
