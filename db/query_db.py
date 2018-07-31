import sqlite3
import pymysql
from flask import g

DATABASE = './db/taskDB.db'

# def query_db(query, args=(), one=False):
#     cur = g.db.execute(query, args)
#     rv = [dict((cur.description[idx][0], value)
#                for idx, value in enumerate(row)) for row in cur.fetchall()]
#     return (rv[0] if rv else None) if one else rv


def query_db_outside(query, args=(), one=False):
    db = sqlite3.connect(DATABASE)
    cur = db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    db.commit()
    db.close()
    return (rv[0] if rv else None) if one else rv

# def query_db_outside(query, args=[], one=False):
#     db = pymysql.connect("localhost", "root", "sure", "taskDB", 3306)
#     cur = db.cursor()
#     cur.execute(query, args)
#     rv = [dict((cur.description[idx][0], value)
#                for idx, value in enumerate(row)) for row in cur.fetchall()]
#     db.commit()
#     db.close()
#     return (rv[0] if rv else None) if one else rv