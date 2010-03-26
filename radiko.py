#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
#from uuid import uuid4
import os
import os.path
import logging

import time, random, md5
def uuid( *args ):
    t = long( time.time() * 1000 )
    r = long( random.random()*100000000000000000L )
    try:
        a = socket.gethostbyname( socket.gethostname() )
    except:
        # if we can't get a network address, just imagine one
        a = random.random()*100000000000000000L
    data = str(t)+' '+str(r)+' '+str(a)+' '+str(args)
    data = md5.md5(data).hexdigest()
    return data

class Radiko(object):
    def __init__(self, storage, name, channel, **other):
        self.storage = storage
        self.name    = name
        self.channel = channel
        self.other   = other

    def __call__(self, time, airtime):
        if not os.path.exists('audio'):
            os.makedirs('audio')
        path = "audio/%s.aac" % uuid()
        cmd = """
rtmpdump -B %d -y "simul-stream" -n "radiko.smartstream.ne.jp" -c 1935
 -s "http://radiko.jp/player/player_0.0.9.swf"
 -p "http://radiko.jp/player/player.html#QRR"
 -a "QRR/_defInst_" -f "WIN 10,0,45,2" -v -o -
 | ffmpeg -y -i - -acodec copy %s
""".replace("\n","") % (airtime.seconds, path)
        ret = os.system("echo '%s'" % cmd)
        if ret == 0:
            self.storage.add(self.name, time, path, self.other)
