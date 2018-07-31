from flask import Blueprint, request, jsonify
from redis import Redis

from db.query_db import query_db_outside
from .sql import query

log = Blueprint('log', __name__)
redis = Redis()

# 查询task列表
@log.route('/list',methods=['POST','GET'])
def selectTaskListByUserId():
    sessionid = request.args.get('sessionid')
    userid = getuserid(sessionid)

    taskList = query_db_outside(query['select_tasklist'],(userid,))
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': taskList})

# 按条件筛选task
@log.route('/filtrate',methods=['POST','GET'])
def filtrateSelect():
    freqency = request.form.get('freqency')
    enabled = request.form.get('enabled')
    category = request.form.get('category')
    sessionid = request.args.get('sessionid')
    userid = getuserid(sessionid)
    if freqency == '':
        freqency = None
    if enabled == '':
        enabled = None
    if category == '':
        category = None

    taskList = query_db_outside(query['filtrateSelect'], (userid,freqency,enabled,category,))
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': taskList})

# 查看任务详情
@log.route('/select',methods=['POST'])
def selectById():
    taskid = request.form.get('taskid')
    task = query_db_outside(query['select_task'], (taskid,))
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': task})

# 查询特定task的运行记录
@log.route('/selctTaskLogById',methods=['POST'])
def selectTaskLogByTaskId():
    taskid = request.form.get('taskid')
    task = query_db_outside(query['selctTaskLogById'], (taskid,))
    date = []
    result = []
    tasktable = task.copy()
    task.reverse()
    for i in task:
        date.append(i['run_time'])
        result.append(i['result'])

    return jsonify({'code':200,'message':'ok','data':{'tab_data':tasktable,'chart_data':{'run_time':date,'result':result}}})

# 修改comments
@log.route('/updateComment',methods=['POST'])
def selectHistoryById():
    id = request.form.get('id')
    comments = request.form.get('comments')
    taskList = query_db_outside(query['updateComment'], (comments,id,))
    return jsonify({'code': 200, 'message': 'ok', 'data': ''})

#查询errortask 通过时间
@log.route('/error_list',methods=['GET','POST'])
def selectErrorTaskByResulttime():
    date = request.form.get('date')
    fre = request.form.get('fre')
    sessionid = request.form.get('sessionid')
    userid = getuserid(sessionid)

    taskList = []
    if fre == 'daily':
      taskList = query_db_outside(query['SelectDailyErrorList'], (date,userid,))
    if fre == 'weekly':
      taskList = query_db_outside(query['SelectWeeklyErrorList'], (date,userid,))
    if fre == 'monthly':
      taskList = query_db_outside(query['SelectMonthlyErrorList'], (date,userid,))
    return jsonify({'code': 200, 'message': 'ok', 'data': taskList})

#查询特定模块的errortask 通过时间
@log.route('/spe_error_list',methods=['GET','POST'])
def selectSpeErrorTaskByResulttime():
    date = request.form.get('date')
    fre = request.form.get('fre')
    module = request.form.get('module')
    sessionid = request.args.get('sessionid')
    userid = getuserid(sessionid)

    taskList = []
    if fre == 'daily':
        taskList = query_db_outside(query['SelectSpeDailyErrorList'], (date,module,userid,))
    if fre == 'weekly':
        taskList = query_db_outside(query['SelectSpeWeeklyErrorList'], (date,module,userid,))
    if fre == 'monthly':
        taskList = query_db_outside(query['SelectSpeMonthlyErrorList'], (date,module,userid,))
    return jsonify({'code': 200, 'message': 'ok', 'data': taskList})

@log.route('/selectTasks',methods=['GET','POST'])
def selectTasks():

    owner = request.form.get('owner')
    taskList = query_db_outside(query['SelectTaskOfMike'], (owner,))
    return jsonify({'code': 200, 'message': 'ok', 'data': taskList})

def getuserid(sessionid):
    if redis.get(sessionid) is not None:
        return redis.get(sessionid).decode()
    else:
        return redis.get(sessionid)

# @log.before_request
# def before_request():
#     sessionid = request.args.get('sessionid')
#     if sessionid is None:
#         sessionid = request.form.get('sessionid')
#     userid = redis.get(sessionid)
#     if userid is None:
#         return jsonify({'code': 401, 'meaasge': 'No This User', 'data': ''})