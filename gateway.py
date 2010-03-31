#!/usr/bin/env python
# -*- coding: utf-8; mode:python-*-
import tempita
import os.path
import traceback
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
        items =  self.storage.list()
        for item in items:
            if not 'title' in item:
                item['title'] = item['name']

        self.response(200)
        return template('index', items=items)

    def on_podcast(self):
        name  = self.get('name')
        items = []
        for item in self.storage.find_by_name(name):
            try:
                if not 'title' in item:
                    item['title'] = item['name']
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
        try:
            return self.__getattribute__("on_%s" % self.get('m', 'index'))()
        except Exception,e:
            self.response(500)
            return template('error',
                            error=str(e),
                            trace=escape(traceback.format_exc()))

    def get(self, name, default=None):
        return self.parameters.get(name, [ default ])[0]

    def response(self, code=200, type='text/html'):
        status = { 200: '200 OK',
                   500: '500 Internal Server Error'}[code]
        response_headers = [('Content-type', type)]
        self.start_response(status, response_headers)

