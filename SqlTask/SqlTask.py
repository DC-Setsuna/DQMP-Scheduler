import ibm_db
import sys
import json
from db.query_db import query_db_outside
from .sql import query
import time
from functools import wraps


def run(user_id, taskid, content, freqency, threshold, taskname, category, description):
    print('\033[4;32m' + 'Start to running <' + taskname + '> [id:' + taskid + ']' + '\033[0m')
    config = open(sys.path[0] + '/SqlTask/config.json', 'r')
    config = config.read()
    config = json.loads(config)
    result_time = time.strftime('%Y-%m-%d', time.localtime())
    insert_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    dns = "DATABASE=%s;HOSTNAME=%s;PORT=%s;PROTOCOL=TCPIP;UID=%s;PWD=%s" % (
        config['database'], config['hostname'], config['port'], config['user_id'], config['password'])
    try:
        conn = ibm_db.connect(dns, "", "")
        sql = content
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_assoc(stmt)
    except:
        query_db_outside(query['tasklog'], (taskname, taskid, '0', 'DB error', insert_time,))
        return

    result_count = int(result['1'])


    table = {'daily': 'add_dailylog',
             'weekly': 'add_weeklylog',
             'monthly': 'add_monthlylog'}

    if result_count > threshold:
        daily_status = 'Fail'
        resulttab_status = 'Fail'
        print('\033[1;33;41m<' + taskname + '> [id:' + taskid + ']' + 'Exceed the threshold [count:' + str(result_count) + ']' + '\033[0m')
    else:
        daily_status = 'Success'
        resulttab_status = 'Success'
        print('\033[1;30;47m<' + taskname + '> [id:' + taskid + ']' + 'success!' + '\033[0m')

    query_db_outside(query[table[freqency]], (taskid, result_count, result_time, daily_status, user_id, insert_time, taskname, category, description,))
    query_db_outside(query['add_resulttab'], (taskname, taskid, result_count, resulttab_status, insert_time, '10s',))
