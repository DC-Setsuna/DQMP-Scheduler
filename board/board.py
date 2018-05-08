import sqlite3
import sys
from db.query_db import query_db
from flask import Blueprint, jsonify
from .sql import query
from file.file import dict_factory

board = Blueprint('board', __name__)

# 查询daily数据
@board.route('/daily_list', methods=['POST'])
def selectDailyListByUserId():
    conn = sqlite3.connect(sys.path[0] + '/db/taskDB.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    # 查询数据
    # sql = "select run_time as Statistictime ,ifnull((select SUM(account) FROM dailylog a WHERE a.run_time = dailylog.run_time),0) as Totalnumberoftasks,ifnull((select SUM(account) FROM dailylog b where status=0 AND b.run_time = dailylog.run_time ),0) as Totalnumberoferrortasks from dailylog GROUP BY run_time"
    # cursor.execute(sql)
    # dailyList = cursor.fetchall()
    # conn.close()

    dailyList = query_db(query['select_daily'])

    daily_date_list=[]
    daily_data = []
    daily_err = []

    for i in range(len(dailyList)):
      daily_date_list.append(dailyList[i]['Statistictime'])
      daily_data.append(dailyList[i]['Totalnumberoftasks'])
      daily_err.append(dailyList[i]['Totalnumberoferrortasks'])

    dailyLists = []
    dailyLists.append(daily_date_list)
    dailyLists.append(daily_data)
    dailyLists.append(daily_err)
    return jsonify({'code': 200, 'meaasge': '', 'data': {'tabData':dailyList,'chartData':dailyLists}})

# 查询weekly数据
@board.route('/weekly_list', methods=['POST'])
def selectWeeklyByUserId():
    dailyList = query_db(query['select_daily'])

    daily_date_list = []
    daily_data = []
    daily_err = []

    for i in range(len(dailyList)):
        daily_date_list.append(dailyList[i]['Statistictime'])
        daily_data.append(dailyList[i]['Totalnumberoftasks'])
        daily_err.append(dailyList[i]['Totalnumberoferrortasks'])

    dailyLists = []
    dailyLists.append(daily_date_list)
    dailyLists.append(daily_data)
    dailyLists.append(daily_err)
    return jsonify({'code': 200, 'meaasge': '', 'data': {'tabData': dailyList, 'chartData': dailyLists}})