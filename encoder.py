#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import threading
import logging
import os
import time
from uuid import uuid4
from Queue import Queue

class Encoder(object):
    def __init__(self, storage):
        self.storage = storage
        self.q = Queue(3)
        def f():
            logging.info("start encoding thread")
            while True:
                try:
                    f = self.q.get(block=True)
                    logging.info("encoding pop")
                    f()
                    logging.info("encoding done")
                except Exception, e:
                    logging.error(e)
                    logging.error(traceback.format_exc())
        t = threading.Thread(target=f)
        t.setDaemon(True)
        t.start()

    def add(self, entry):
        def f():
            if not os.path.exists('audio'):
                os.makedirs('audio')
            path = "audio/%s.m4a" % uuid4().hex
            cmd = "ffmpeg -y -i %s %s" % (entry['original'], path)
            logging.info(cmd)
            ret = os.system(cmd)
            if ret == 0:
                self.storage.transaction(
                    lambda : self.storage.update(entry['id'], path))
        self.q.put(f, block=True)
