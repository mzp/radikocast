#!/usr/bin/env python
# -*- coding: utf-8; mode:python-*-
from wsgiref.handlers import CGIHandler
from wsgiref.util import *
from cgi import parse_qs, escape
import tempita
from storage import Storage

class application(object):
    def on_index(self, environ, start_response):
        storage = Storage('storage.db')
        programs = storage.find_all()
        status = '200 OK'
        response_headers = [('Content-type','text/html')]
        start_response(status, response_headers)
        with file('templates/index.html') as io:
            t = tempita.Template(io.read())
            return t.substitute(programs=programs)

    def __call__(self, environ, start_response):
        parameters = parse_qs(environ.get('QUERY_STRING', ''))
        page = parameters.get('m', ['index'])[0]
        return self.__getattribute__("on_%s" % page)(environ, start_response)
