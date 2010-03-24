#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import sqlite3
import os.path
import pickle
from base64 import *

class Storage(object):
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            self.execute__(lambda db: db.execute("""
create table podcasts(
   id integer primary key,
   created_at int,
   name text,
   path text,
   object blob
);
"""))

    def add(self, **args):
        self.execute__(lambda db: db.execute("insert into podcasts(id,name,path,object) values(null,?,?,?)",
                                             (args['name'], args['path'], self.dump__( args ))))

    def find_by_path(self, path):
        def f(db):
            one = db.execute("select object from podcasts where path = ?", [ path ]).fetchone()
            return self.load__(one[0]) if one != None else None

        return self.execute__(f)

    def execute__(self, f):
        db = sqlite3.connect(self.path)
        try:
            res = f(db)
            db.commit()
            return res
        finally:
            db.close()

    def dump__(self, s):
        return b64encode( pickle.dumps(s) )

    def load__(self, s):
        return pickle.loads(b64decode(s))
