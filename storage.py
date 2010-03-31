#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import sqlite3
import os.path
import pickle
import threading
import logging
import broadcast
import traceback
from Queue import Queue
from base64 import *

class Storage(object):
    def __init__(self, path):
        self.path = path
        self.broadcast = broadcast.broadcast()
        if not os.path.exists(path):
            self.execute__(lambda db: db.execute("""CREATE TABLE podcasts(
                                                            id integer primary key not null,
                                                            name text not null,
                                                            path text,
                                                            original text not null,
                                                            created_at integer not null,
                                                            object blob not null);"""))
        self.q = Queue(3)
        def f():
            while True:
                try:
                    f = self.q.get(block=True)
                    logging.info("transaction pop")
                    f()
                except Exception, e:
                    logging.error(e)
                    logging.error(traceback.format_exc())

        t = threading.Thread(target=f)
        t.setDaemon(True)
        t.start()

    def transaction(self,f):
        self.q.put(f, block=True)


    def add(self, name,created_at, original, path=None, obj={}):
        def f(db):
            dump = self.dump__( obj )
            db.execute("""
INSERT INTO podcasts(id  ,name, created_at, original, path, object)
              VALUES(null,   ?,          ?,        ?,    ?,      ?)""",
                       (  name, created_at, original, path, dump))
            return db.execute("SELECT last_insert_rowid()").fetchone()[0]
        obj['name']       = name
        obj['created_at'] = created_at
        obj['path']       = path
        obj['original']   = original
        id = self.execute__(f)
        self.broadcast(self.find_by_id(id))

    def find_by_name(self, name):
        def f(db):
            cur = db.execute("""SELECT id, path, object FROM podcasts
                                                        WHERE name = ? AND path NOTNULL
                                                        ORDER BY created_at DESC""",
                             [ name ])
            return map(lambda args: self.load_obj(*args), cur.fetchall())
        return self.execute__(f)

    def find_by_id(self, id):
        def f(db):
            cur = db.execute("""SELECT id, path, object FROM podcasts
                                                        WHERE id = ?
                                                        ORDER BY created_at DESC""",
                             [ id ])
            return self.load_obj(*cur.fetchone())
        return self.execute__(f)

    def find_incomplete(self):
        def f(db):
            cur = db.execute("""SELECT id, path, object FROM podcasts
                                                        WHERE path ISNULL
                                                        ORDER BY created_at ASC""",[])
            return map(lambda args: self.load_obj(*args), cur.fetchall())
        return self.execute__(f)

    def list(self):
        def f(db):
            cur = db.execute("""SELECT id, path, object FROM podcasts
                                                        WHERE path NOTNULL
                                                        GROUP BY name
                                                        ORDER BY created_at DESC""",[])
            return map(lambda args: self.load_obj(*args), cur.fetchall())
        return self.execute__(f)

    def update(self, id, path):
        def f(db):
            db.execute("UPDATE podcasts SET path = ? WHERE id = ?",
                       [ path, id ])
        self.execute__(f)

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

    def load_obj(self, id, path, obj):
        item = self.load__(obj)
        item['id']   = id
        item['path'] = path
        return item

    def listen(self, f):
        self.broadcast += f

