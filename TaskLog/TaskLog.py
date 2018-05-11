from flask import Blueprint, request, jsonify
from db.query_db import query_db_outside
from .sql import query

tasklog = Blueprint('tasklog', __name__)

# 查询task列表
@tasklog.route('/list',methods=['POST'])
def selectTaskListByUserId():
    taskList = query_db_outside(query['select_tasklist'])
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': taskList})

# 按条件筛选task
@tasklog.route('/filtrate',methods=['POST'])
def filtrateSelect():
    freqency = request.form.get('freqency')
    enabled = request.form.get('enabled')
    category = request.form.get('category')
    sql = "SELECT * ,(select COUNT(taskid) from result_tab a WHERE a.taskid = task.taskid) as totalrun,(select COUNT(taskid) from result_tab a WHERE a.taskid = task.taskid And a.status = 0) as totalfails From task WHERE owner = 'Account'"

    if freqency:
        sql += " AND freqency = '" + freqency + "'"
    if enabled:
        sql += " AND enabled = '" + enabled + "'"
    if category:
        sql += " AND category = '" + category + "'"

    taskList = query_db_outside(sql)

    return jsonify({'code': 200, 'meaasge': 'ok', 'data': taskList})

# 查看任务详情
@tasklog.route('/select',methods=['POST'])
def selectById():
    taskid = request.form.get('taskid')

    task = query_db_outside(query['select_task'], (taskid,))

    return jsonify({'code': 200, 'meaasge': 'ok', 'data': task})

# 查询特定task的运行记录
@tasklog.route('/selctTaskLogById',methods=['POST'])
def selectTaskLogByTaskId():
    taskid = request.form.get('taskid')

    task = query_db_outside(query['selctTaskLogById'], (taskid,))

    return jsonify({'code':200,'message':'ok','data':task})

# 查询任务history
@tasklog.route('/select_history',methods=['POST'])
def selectHistoryById():
    return jsonify({'code': 200, 'message': 'ok', 'data': ''})