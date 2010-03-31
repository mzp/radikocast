#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-

from storage import *
from nose.tools import *
import os

def ok(expect, actual):
    if 'id' in actual:
        del actual['id']
    if 'path' in actual and actual['path'] == None:
        del actual['path']
    eq_(expect, actual)


class TestStorage:
    def setUp(self):
        try:
            os.remove('test.db')
        except:
            pass

        self.storage = Storage('test.db')
        self.p1 = { 'name'       : "program1",
                    'created_at' : 1,
                    'original'   : "1.aac",
                    'path'       : "1.mp3" }
        self.p2 = { 'name'       : "program1",
                    'created_at' : 2,
                    'original'   : "2.aac",
                    'path'       : "2.mp3" }
        self.p3 = { 'name'       : "program2",
                    'created_at' : 1,
                    'original'   : "3.aac",
                    'path'       : "3.mp3" }
        self.p4 = { 'name'       : "program1",
                    'created_at' : 3,
                    'original'   : "4.aac" }
        self.p5 = { 'name'       : "program1",
                    'created_at' : 4,
                    'original'   : "5.aac" }
        self.p6 = { 'name'       : "program2",
                    'created_at' : 5,
                    'original'   : "6.aac" }

        self.storage.add(**self.p1)
        self.storage.add(**self.p2)
        self.storage.add(**self.p3)
        self.storage.add(**self.p4)
        self.storage.add(**self.p5)
        self.storage.add(**self.p6)

    def tearDown(self):
        os.remove('test.db')

    def test_list(self):
        (p2, p3) = self.storage.list()
        ok(self.p2, p2)
        ok(self.p3, p3)

    def test_find_by_name(self):
        print self.storage.find_by_name("program1")
        (p2, p1) = self.storage.find_by_name("program1")
        ok(self.p1, p1)
        ok(self.p2, p2)

    def test_find_by_id(self):
        (p1,) = self.storage.find_by_id(1)
        print p1
        eq_(1, p1['id'])
        ok( self.p1, p1)

        (p4,) = self.storage.find_by_id(4)
        eq_(4, p4['id'])
        ok( self.p4, p4)

    def test_find_incomplete(self):
        (p4, p5, p6) = self.storage.find_incomplete()
        ok( self.p4, p4)
        ok( self.p5, p5)
        ok( self.p6, p6)

    def test_update(self):
        self.storage.update(4, '4.mp3')
        (p4,) = self.storage.find_by_id(4)
        eq_( '4.mp3', p4['path'])

        (p5, p6) = self.storage.find_incomplete()
        ok( self.p5, p5)
        ok( self.p6, p6)
