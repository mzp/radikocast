#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import threading
import logging
import os
from uuid import uuid4
from Queue import Queue

class Encoder(object):
    def __init__(self, storage):
        self.storage = storage
        self.q = Queue(3)
        def f():
            while True:
                try:
                    f = self.q.get(block=True)
                    logging.info("encoding pop")
                    f()
                except Exception, e:
                    print e
        t = threading.Thread(target=f)
        t.setDaemon(True)
        t.start()

    def add(self, entry):
        def f():
            if not os.path.exists('audio'):
                os.makedirs('audio')
            path = "audio/%s.aac" % uuid4().hex
            cmd = "ffmpeg -y -i %s %s" % (entry['original'], path)
            logging.info(cmd)
            ret = os.system("%s" % cmd)
            if ret == 0:
                self.storage.transaction(
                    lambda : self.storage.update(entry['id'], path))
        self.q.put(f, block=True)
