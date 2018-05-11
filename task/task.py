from flask import Blueprint, request, jsonify
from db.query_db import query_db_outside
from .sql import query
from SqlTask.SqlTask import run
import time
import __main__



task = Blueprint('task', __name__)

@task.route('/add/', methods=['GET', 'POST'])
def add_task():
    # scheduler.add_job(interval_job, trigger='interval', seconds=5, id='interval_id2')
    # scheduler.add_job(func=interval_job, id='123', trigger='interval', seconds=5)
    # sqlTask = SqlTask.SqlTask()
    # scheduler.add_job(func=interval_job, id='sqlaa', trigger='interval', seconds=100)
    print(request.form)
    taskid = request.form.get('taskid')
    print(taskid)
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
    upload_user_id = int(request.form.get('upload_user_id'))

    upload_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    cur = query_db_outside(query['add_task'], (taskid, category, owner, email,
                                       description, tag, enabled, freqency,
                                       task_type, threshold, filepath, upload_time,
                                       update_time, upload_user_id))
    if run_now:
        run(user_id=upload_user_id, taskid=taskid, filepath=filepath, freqency=freqency)

    if enabled:
        if freqency == 'daily':
            __main__.scheduler.add_job(func=run, kwargs={'user_id':upload_user_id, 'taskid':taskid, 'filepath':filepath, 'freqency':freqency}, id=taskid, trigger='interval', seconds=20)
            pass
    return jsonify({'code': 200 })