import datetime

from flask import Blueprint, request, jsonify
from redis import Redis

from db.query_db import query_db_outside
from .sql import query

log = Blueprint('log', __name__)
redis = Redis()

# 查询task列表
@log.route('/list',methods=['POST','GET'])
def selectTaskListByUserId():
    taskList = query_db_outside(query['select_tasklist'])
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': taskList})

# 按条件筛选task
@log.route('/filtrate',methods=['POST','GET'])
def filtrateSelect():
    freqency = request.form.get('freqency')
    enabled = request.form.get('enabled')
    category = request.form.get('category')
    if freqency == '':
        freqency = None
    if enabled == '':
        enabled = None
    if category == '':
        category = None

    taskList = query_db_outside(query['filtrateSelect'], (freqency,enabled,category,))
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

    taskList = []
    if fre == 'daily':
      taskList = query_db_outside(query['SelectDailyErrorList'], (date,))
    if fre == 'weekly':
      taskList = query_db_outside(query['SelectWeeklyErrorList'], (date,))
    if fre == 'monthly':
      taskList = query_db_outside(query['SelectMonthlyErrorList'], (date,))
    return jsonify({'code': 200, 'message': 'ok', 'data': taskList})

#查询特定模块的errortask 通过时间
@log.route('/spe_error_list',methods=['GET','POST'])
def selectSpeErrorTaskByResulttime():
    date = request.form.get('date')
    fre = request.form.get('fre')
    module = request.form.get('module')

    taskList = []
    if fre == 'daily':
        taskList = query_db_outside(query['SelectSpeDailyErrorList'], (date,module,))
    if fre == 'weekly':
        taskList = query_db_outside(query['SelectSpeWeeklyErrorList'], (date,module,))
    if fre == 'monthly':
        taskList = query_db_outside(query['SelectSpeMonthlyErrorList'], (date,module,))
    return jsonify({'code': 200, 'message': 'ok', 'data': taskList})

@log.route('/selectTasks',methods=['GET','POST'])
def selectTasks():

    owner = request.form.get('owner')
    taskList = query_db_outside(query['SelectTaskOfMike'], (owner,))
    return jsonify({'code': 200, 'message': 'ok', 'data': taskList})

# 通过username，查询出个人的task以及前八条tasklog
@log.route('/getTasklogByUsername',methods=['GET'])
def getTasklogByUsername():
    sessionid = request.args.get('sessionid')
    category = request.args.get('category')
    userid = getuserid(sessionid)

    username = query_db_outside(query['getUsernameByUserid'], (userid,))
    taskLog = query_db_outside(query['getTaskinfoByUsername'], (username[0]['name'],category,))
    today = str(datetime.date.today()) + " 23:59:59"
    beforeEightDay = str(datetime.date.today() - datetime.timedelta(days=8)) + " 00:00:00"
    resultLog = query_db_outside(query['getTasklogByUsername'], (username[0]['name'],category,beforeEightDay,today,))

    workList = []
    for i in taskLog:
        tasklist = {'taskid':'', 'taskname': '', 'description': ''}
        for j in resultLog:
            if j['taskname'] == i['taskname']:
                tasklist.update({j['run_time'][0:10]:j['result']})
        tasklist['taskid'] = i['taskid']
        tasklist['taskname'] = i['taskname']
        tasklist['description'] = i['description']
        if str(datetime.date.today()) in tasklist.keys():
            if str(datetime.date.today() - datetime.timedelta(days=1)) in tasklist.keys():
                change = tasklist[str(datetime.date.today())] - tasklist[str(datetime.date.today() - datetime.timedelta(days=1))]
                tasklist.update({'change':change})
                if(tasklist[str(datetime.date.today() - datetime.timedelta(days=1))] == 0):
                    tasklist.update({'percent':''})
                else:
                    if change < 0:
                        change = -change
                    tasklist.update({'percent':str(round(change/tasklist[str(datetime.date.today() - datetime.timedelta(days=1))]*100,2))+'%'})
            else:
                tasklist.update({'change':''})
        else:
            tasklist.update({'change':''})
            tasklist.update({'percent':''})

        workList.append(tasklist)
    return jsonify({'code': 200, 'message': 'ok', 'result': workList})

# 通过username查出个人的所有类别
@log.route('/getCategoryByUsername',methods=['GET'])
def getCategaryByUsername() :
    sessionid = request.args.get('sessionid')
    userid = getuserid(sessionid)
    username = query_db_outside(query['getUsernameByUserid'], (userid,))

    categoryList = query_db_outside(query['getCategoryByUsername'], (username[0]['name'],))
    return jsonify({'code': 200, 'message': 'ok', 'category': categoryList})

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