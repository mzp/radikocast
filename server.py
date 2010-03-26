#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
from gateway import application
from wsgiref.simple_server import make_server

if __name__ == '__main__':
    print "serving http on port 8000..."
    make_server('', 8000, application()).serve_forever()

