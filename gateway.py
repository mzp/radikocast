#!/usr/bin/env python
# -*- coding: utf-8; mode:python-*-
import tempita
import os.path
from wsgiref.handlers import CGIHandler
from wsgiref.util import *
from cgi import parse_qs, escape
from storage import Storage

def template(template, **d):
    with file("templates/%s.html" % template) as io:
        t = tempita.Template(io.read())
        return t.substitute(**d)

class application(object):
    def __init__(self):
        self.storage = Storage('storage.db')

    def on_index(self):
        programs = self.storage.find_all()
        self.response(200)
        return template('index', programs=programs)

    def on_podcast(self):
        name  = self.get('name')
        items = []
        for item in self.storage.find_by_name(name):
            try:
                item['size'] = os.path.getsize(item['path'])
                item['type'] = 'audio/aac'
                items.append(item)
            except:
                pass

        self.response(200, 'application/rss+xml')
        return template('podcast',
                        name  = name,
                        link  = escape("?m=podcast&name=%s" % name),
                        items = items)

    def __call__(self, environ, start_response):
        self.parameters     = parse_qs(environ.get('QUERY_STRING', ''))
        self.environ        = environ
        self.start_response = start_response
        return self.__getattribute__("on_%s" % self.get('m', 'index'))()

    def get(self, name, default=None):
        return self.parameters.get(name, [ default ])[0]

    def response(self, code=200, type='text/html'):
        status = { 200: '200 OK' }[code]
        response_headers = [('Content-type', type)]
        self.start_response(status, response_headers)

