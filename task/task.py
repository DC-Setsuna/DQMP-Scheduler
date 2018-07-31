import datetime

from flask import Blueprint, request, jsonify
from redis import Redis

from db.query_db import query_db_outside
from .sql import query
from SqlTask.SqlTask import run
import time
import uuid
import __main__

task = Blueprint('task', __name__)
redis = Redis()

@task.route('/add/', methods=['GET', 'POST'])
def add_task():
    taskid = str(uuid.uuid1()) #request.form.get('taskid')
    category = request.form.get('category')
    owner = request.form.get('owner')
    email = request.form.get('email')
    description = request.form.get('description')         # The description of the task
    tag = request.form.get('tag')                         # The tag of the task
    enabled = eval(request.form.get('enabled'))               # Whether the available
    freqency = request.form.get('freqency')
    task_type = request.form.get('task_type')
    threshold = int(request.form.get('threshold'))             # The threshold of result for sending the notice to owner
    filepath = request.form.get('file_path')              # The path of the task need to run
    run_now = eval(request.form.get('run_now'))           # just run now
    content = request.form.get('content')
    upload_user_id = int(redis.get(request.form.get('upload_user_id')).decode())
    taskname = request.form.get('taskname')

    upload_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    query_db_outside(query['add_task'], (taskid, category, owner, email,
                                       description, tag, enabled, freqency,
                                       task_type, threshold, filepath, upload_time,
                                       update_time,content, upload_user_id,taskname,))
    if run_now:
        __main__.scheduler.add_job(func=run, kwargs={
                'user_id': upload_user_id,
                'taskid': taskid,
                'content': content,
                'freqency': freqency,
                'threshold': threshold,
                'taskname': taskname,
                'category': category,
                'description': description}, id=str(uuid.uuid1()), trigger='date', name=taskname, misfire_grace_time=60 * 60 * 24,
                                   run_date=datetime.datetime.now() + datetime.timedelta(seconds=3))

    if enabled:
        if freqency == 'daily':
            __main__.scheduler.add_job(func=run, kwargs={
                'user_id':upload_user_id,
                'taskid':taskid,
                'content':content,
                'freqency':freqency,
                'threshold': threshold,
                'taskname': taskname,
                'category': category,
                'description': description}, id=taskid, trigger='interval', days=1, name=taskname, misfire_grace_time=60 * 60 * 24)
        if freqency == 'weekly':
            __main__.scheduler.add_job(func=run, kwargs={
                'user_id': upload_user_id,
                'taskid': taskid,
                'content': content,
                'freqency': freqency,
                'threshold': threshold,
                'taskname': taskname,
                'category': category,
                'description': description}, id=taskid, trigger='interval', weeks=1, name=taskname, misfire_grace_time=60 * 60 * 24)
        if freqency == 'monthly':
            __main__.scheduler.add_job(func=run, kwargs={
                'user_id': upload_user_id,
                'taskid': taskid,
                'content': content,
                'freqency': freqency,
                'threshold': threshold,
                'taskname': taskname,
                'category': category,
                'description': description}, id=taskid, trigger='interval', days=30, name=taskname, misfire_grace_time=60 * 60 * 24)
    #status
    return jsonify({'code': 200 })

#在task被更新后，时间会被重新安排，错过一次执行，update不应该影响时间
@task.route('/update/', methods=['GET', 'POST'])
def reschedule_task():
    taskid = request.form.get('taskid')
    category = request.form.get('category')
    owner = request.form.get('owner')
    email = request.form.get('email')
    description = request.form.get('description')  # The description of the task
    tag = request.form.get('tag')  # The tag of the task
    freqency = request.form.get('freqency')
    task_type = request.form.get('task_type')
    threshold = int(request.form.get('threshold'))  # The threshold of result for sending the notice to owner
    #filepath = request.form.get('file_path')  # The path of the task need to run
    content = request.form.get('content')
    upload_user_id = int(request.form.get('upload_user_id'))
    taskname = request.form.get('taskname')
    enabled = eval(request.form.get('enabled'))

    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    query_db_outside(query['update_task'], (category, owner, email,
                                       description, tag, freqency,
                                       task_type, threshold, content,
                                       update_time, upload_user_id, taskname, taskid,))
    if enabled:
        __main__.scheduler.remove_job(taskid)

        if freqency == 'daily':
            __main__.scheduler.add_job(func=run, kwargs={
                'user_id': upload_user_id,
                'taskid': taskid,
                'content': content,
                'freqency': freqency,
                'threshold': threshold,
                'taskname': taskname,
                'category': category,
                'description': description}, id=taskid, trigger='interval', days=1, name=taskname, misfire_grace_time=60 * 60 * 24)
        if freqency == 'weekly':
            __main__.scheduler.add_job(func=run, kwargs={
                'user_id': upload_user_id,
                'taskid': taskid,
                'content': content,
                'freqency': freqency,
                'threshold': threshold,
                'taskname': taskname,
                'category': category,
                'description': description}, id=taskid, trigger='interval', weeks=1, name=taskname, misfire_grace_time=60 * 60 * 24)
        if freqency == 'monthly':
            __main__.scheduler.add_job(func=run, kwargs={
                'user_id': upload_user_id,
                'taskid': taskid,
                'content': content,
                'freqency': freqency,
                'threshold': threshold,
                'taskname': taskname,
                'category': category,
                'description': description}, id=taskid, trigger='interval', days=30, name=taskname, misfire_grace_time=60 * 60 * 24)

    return jsonify({'code': 200})


@task.route('/delete/', methods=['GET', 'POST'])
def delete_task():
    taskid = request.form.get('taskid')
    __main__.scheduler.remove_job(taskid)
    query_db_outside(query['remove_task'], (taskid,))
    return jsonify({'code': 200})


@task.route('/run/', methods=['GET', 'POST'])
def run_task():
    taskid = request.form.get('taskid')
    freqency = request.form.get('freqency')
    threshold = int(request.form.get('threshold'))  # The threshold of result for sending the notice to owner
    content = request.form.get('content')  # The path of the task need to run
    upload_user_id = int(request.form.get('upload_user_id'))
    taskname = request.form.get('taskname')
    category = request.form.get('category')
    description = request.form.get('description')

    __main__.scheduler.add_job(func=run, kwargs={
        'user_id': upload_user_id,
        'taskid': taskid,
        'content': content,
        'freqency': freqency,
        'threshold': threshold,
        'taskname': taskname,
        'category': category,
        'description': description}, id=str(uuid.uuid1()), trigger='date', name=taskname, misfire_grace_time=60 * 60 * 24,
                               run_date=datetime.datetime.now() + datetime.timedelta(seconds=3))

    return jsonify({'code': 200, 'meaasge': 'Task Start', 'data': ''})
