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
   name text,
   path text,
   created_at integer,
   object blob
);
"""))

    def add(self, **args):
        self.execute__(lambda db: db.execute("insert into podcasts(id,name,created_at, path,object) values(null,?,?,?,?)",
                                             (args['name'], args['created_at'], args['path'], self.dump__( args ))))

    def find_by_path(self, path):
        def f(db):
            one = db.execute("select object from podcasts where path = ?", [ path ]).fetchone()
            return self.load__(one[0]) if one != None else None
        return self.execute__(f)

    def find_by_name(self, name):
        def f(db):
            cur = db.execute("select object from podcasts where name = ? order by created_at desc",
                             [ name ])
            return map(lambda s: self.load__(s[0]), cur.fetchall())
        return self.execute__(f)

    def find_all(self):
        def f(db):
            res = []
            for name in db.execute("select name from podcasts group by name order by name").fetchall():
                cur = db.execute("select object from podcasts where name = ? order by created_at desc", name)
                res.append((name[0],
                            map(lambda s: self.load__(s[0]), cur.fetchall())))
            return res
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
