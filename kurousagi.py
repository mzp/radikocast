#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import urllib2
import re
import os
import os.path
import logging
from urlparse import urlparse
from uuid import uuid4
from xml.dom.minidom import parseString

def basename(url):
    path = urlparse(url).path
    return os.path.basename(path)

def get(url):
    try:
        with file(url) as f:
            return f.read()
    except:
        return urllib2.urlopen(url).read()

def xml(str):
    return parseString(str)

def mms(url, path):
    cmd = "mimms %s %s" % (url,path)
    logging.info(cmd)
    return os.system(cmd)

def grep(pattern, elements):
    return filter(lambda e: re.search(pattern, e.toxml()) , elements)

def gel(name, dom):
    return dom.getElementsByTagName(name)


class Kurousagi(object):
    def __init__(self, storage, url, **other):
        self.storage = storage
        self.name    = 'kurousagi'
        self.url     = url
        self.other   = other

    def __call__(self, time=None, airtime=None):
        (entry,) = grep(u'黒うさぎ',
                        gel('entry',
                            xml( get( self.url ) )))
        url = gel('Ref', entry)[0].getAttribute('href')

        filename = basename(url)
        path     = "audio/%s.wmv" % uuid4().hex
        if self.storage.exist( self.name, filename):
            return
        if mms(url,path) != 0:
            return
        self.storage.transaction(
            lambda : self.storage.add(name = self.name,
                                      created_at  = int(time.strftime("%s")),
                                      original    = path,
                                      original_name = filename,
                                      obj=self.other))

if __name__ == '__main__':
    import storage
    k = Kurousagi(storage.Storage('test.db'),'http://www.ohsama.tv/playlists/special.asx')
    k()
