#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-

import hashlib

def hashsum(file):
    hash = hashlib.md5()
    s = file.read(1)
    while s != '':
        hash.update(s)
        s = file.read(1)
    return hash.hexdigest()

