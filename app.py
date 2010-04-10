#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import threading
import radiko
import kurousagi
import time_table
import storage
import scheduler
import encoder
import logging

from datetime import datetime
import time
Type = {
    'radiko' : radiko.Radiko,
    'kurousagi' : kurousagi.Kurousagi
}

class Loop(threading.Thread):
    def __init__(self,time, f):
        super(Loop,self).__init__()
        self.time = time
        self.f = f

    def run(self):
        logging.info("start scheduler thread")
        while True:
            try:
                self.f()
                time.sleep(self.time)
            except Exception, e:
                print e

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='radikocast.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(console)

    table     = time_table.open("time_table.yaml")
    storage   = storage.Storage('storage.db')
    encoder   = encoder.Encoder(storage)
    scheduler = scheduler.Scheduler()

    storage.listen(lambda entry: encoder.add(entry))
    for program in table:
        if program['type'] in Type:
            def f(*args):
                agent = Type[program['type']](storage=storage, **program)
                t = threading.Thread(target=lambda: agent(*args))
                t.start()
            scheduler.add(time     = program['time'],
                          airtime  = program['airtime'],
                          at       = program.get('at',None),
                          repeat   = program.get('repeat',None),
                          callback = f)
        else:
            print "unknown type: %s" % type

    t = Loop(30.0, lambda: scheduler.invoke(datetime.now()))
    t.setDaemon(True)
    t.start()

    for entry in storage.find_incomplete():
        encoder.add(entry)

    while True:
        time.sleep(3000)
