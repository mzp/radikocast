#!/opt/local/bin/python
# -*- coding: utf-8; mode:python-*-
from wsgiref.handlers import CGIHandler
from gateway import application

if __name__ == '__main__':
    CGIHandler().run(application())
