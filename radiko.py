#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
from uuid import uuid4

class Radiko(object):
    def __init__(self, storage, name, channel, **other):
        self.storage = storage
        self.name    = name
        self.channel = channel
        self.other   = other

    def __call__(self, time, airtime):
        path = "audio/%s.aac" % uuid4().hex
        cmd = """
rtmpdump -B %d -y "simul-stream" -n "radiko.smartstream.ne.jp" -c 1935
 -s "http://radiko.jp/player/player_0.0.9.swf"
 -p "http://radiko.jp/player/player.html#QRR"
 -a "QRR/_defInst_" -f "WIN 10,0,45,2" -v -o -
 | ffmpeg -y -i - -acodec copy %s
""".replace("\n","") % (airtime.seconds, path)
        print cmd
