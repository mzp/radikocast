#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-

from storage import *
from nose.tools import *
import os
import hashsum

class TestStorage:
    def setUp(self):
        with open('hashsum_test.dat','w') as f:
            f.write("\x01")
            f.write("\x02")
            f.write("\x03")

    def tearDown(self):
        os.remove('hashsum_test.dat')

    def test_checksum(self):
        with open('hashsum_test.dat') as f:
            sum = hashsum.hashsum(f)
            eq_('5289df737df57326fcdd22597afb1fac',sum)
