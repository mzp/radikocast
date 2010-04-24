#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
from uuid import uuid4
import os
import os.path
import logging
from datetime import *

class Radiko(object):
    def __init__(self, storage, channel, **other):
        self.storage = storage
        self.channel = channel
        self.other   = other
        self.templ   = """
rtmpdump --resume -B %d -y "simul-stream" -n "radiko.smartstream.ne.jp" -c 1935
 -s "http://radiko.jp/player/player_0.0.9.swf"
 -p "http://radiko.jp/player/player.html#QRR"
 -a "QRR/_defInst_" -f "WIN 10,0,45,2" -v -o - |
 ffmpeg -y -i - -acodec copy %s
""".replace("\n","")

    def system(self,cmd):
        logging.info(cmd)
        os.system(cmd)

    def __call__(self, time, airtime):
        if not os.path.exists('audio'):
            os.makedirs('audio')
        uuid = uuid4().hex

        # rec
        end = time + airtime
        now = datetime.now()
        count = 0
        while now < end:
            path = "audio/%s-%d.aac" % (uuid, count)
            self.system(self.templ % ((end-now).seconds, path))
            now = datetime.now()
            count += 1

        # concat
        path = "audio/%s.aac" % uuid
        self.system("cat audio/%s-*.aac > %s" % (uuid, path))

        self.storage.transaction(
            lambda : self.storage.add(name       = self.other['name'],
                                      original   = path,
                                      created_at = int(time.strftime("%s")),
                                      obj = self.other))

