import time

from redis import Redis

from db.query_db import query_db_outside
from flask import Blueprint, jsonify, request
from .sql import query
import calendar
import datetime
board = Blueprint('board', __name__)
redis = Redis()

# 查询daily数据
@board.route('/daily_list', methods=['GET','POST'])
def selectDailyListByUserId():
    dailyList = query_db_outside(query['select_daily'])
    dailyTabList = query_db_outside(query["select_daily_desc"])
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': {'tabData':dailyTabList,'chartData':chartList(dailyList)}})
# 查询weekly数据
@board.route('/weekly_list', methods=['GET','POST'])
def selectWeeklyByUserId():
    weeklyList = query_db_outside(query['select_weekly'])
    weeklyTabList = query_db_outside(query['select_weekly_desc'])
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': {'tabData': weeklyTabList, 'chartData': chartList(weeklyList)}})
# 查询monthly数据
@board.route('/monthly_list', methods=['GET','POST'])
def selectMonthlyByUserId():
    monthlyList = query_db_outside(query['monthly_list'])
    monthlyTabList = query_db_outside(query['monthly_list_desc'])
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': {'tabData': monthlyTabList, 'chartData': chartList(monthlyList)}})
#整理monthly/weekly/daily的chart信息
def chartList(list):
    date_list = []
    data_list = []
    err_list = []
    for i in list:
        date_list.append(i['Statistictime'])
        data_list.append(i['Totalnumberoftasks'])
        err_list.append(i['Totalnumberoferrortasks'])
    Lists = []
    Lists.append(date_list)
    Lists.append(data_list)
    Lists.append(err_list)
    return Lists


# 查询daily错误数据，按照模块分组，bashboard右上角
@board.route('/daily_fail_list', methods=['GET','POST'])
def selectFailDailyList():
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
    dailyList = query_db_outside(query['select_fail_daily'])
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': dailyList})
# 查询weekly数据，按照模块分组，bashboard右上角
@board.route('/weekly_fail_list', methods=['GET','POST'])
def selectFailWeekly():
    thisMonday = getThisMonday()
    weeklyList = query_db_outside(query['select_fail_weekly'])
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': weeklyList})
# 查询monthly数据，按照模块分组，bashboard右上角
@board.route('/monthly_fail_list', methods=['GET','POST'])
def selectFailMonthly():
    nowTime = datetime.datetime.now().strftime('%Y-%m')
    monthlyList = query_db_outside(query['monthly_fail_list'])
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': monthlyList})


# 查询特定类别的daily数据
@board.route('/category_daily_list', methods=['GET','POST'])
def selectDailyListByCategory():
    category = request.args.get('category')
    dailyList = query_db_outside(query['category_select_daily'],(category,category,category,))
    dailyTabList = query_db_outside(query['category_select_daily_desc'], (category,category,category,))
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': {'tabData':dailyTabList,'chartData':chartList(dailyList)}})
# 查询特定类别的weekly数据
@board.route('/category_weekly_list', methods=['GET','POST'])
def selectWeeklyByCategory():
    category = request.args.get('category')
    weeklyList = query_db_outside(query['category_select_weekly'],(category,category,category,))
    weeklyTabList = query_db_outside(query['category_select_weekly_desc'], (category, category, category,))
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': {'tabData': weeklyTabList, 'chartData': chartList(weeklyList)}})
# 查询特定类别的monthly数据
@board.route('/category_monthly_list', methods=['GET','POST'])
def selectMonthlyByCategory():
    category = request.args.get('category')
    monthlyList = query_db_outside(query['category_monthly_list'], (category,category,category,))
    monthlyTabList = query_db_outside(query['category_monthly_list_desc'], (category, category, category,))
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': {'tabData': monthlyTabList, 'chartData': chartList(monthlyList)}})


# 查询daily错误数据
@board.route('/category_daily_fail_list', methods=['GET','POST'])
def selectCategoryFailDailyList():
    category = request.args.get('category')
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
    dailyList = query_db_outside(query['category_select_fail_daily'],(category,))
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': dailyList})
# 查询weekly错误数据
@board.route('/category_weekly_fail_list', methods=['GET','POST'])
def selectCategoryFailWeekly():
    category = request.args.get('category')
    thisMonday = getThisMonday()
    weeklyList = query_db_outside(query['category_select_fail_weekly'],(category,))
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': weeklyList})
# 查询monthly错误数据
@board.route('/category_monthly_fail_list', methods=['GET','POST'])
def selectCategoryFailMonthly():
    category = request.args.get('category')
    nowTime = datetime.datetime.now().strftime('%Y-%m')
    monthlyList = query_db_outside(query['category_monthly_fail_list'],(category,))
    return jsonify({'code': 200, 'meaasge': 'ok', 'data': monthlyList})


#查询The job being performed数据
@board.route('/being_performed',methods=['GET','POST'])
def selectBeingPerformed():
    list = query_db_outside(query['select_being_performed'])
    return jsonify({'code':200,'message':'ok','data':list})
#查询error_task数据
@board.route('/error_tasks',methods=['GET','POST'])
def selectExecutionResults():
    list = query_db_outside(query['select_error_tasks'])
    return jsonify({'code':200,'message':'ok','data':list})

#获取本周一日期 年-月-日
def getThisMonday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days = 1)
    m1 = calendar.MONDAY
    while today.weekday() != m1:
        today -= oneday
    nextMonday = today.strftime('%Y-%m-%d')
    return nextMonday

def getuserid(sessionid):
    if redis.get(sessionid) is not None:
        return redis.get(sessionid).decode()
    else:
        return redis.get(sessionid)