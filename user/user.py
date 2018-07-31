from flask import Blueprint, request, jsonify
from db.query_db import query_db_outside
from .sql import query
from redis import Redis

user = Blueprint('user', __name__)
redis = Redis()

@user.route('/getimg', methods=['POST'])
def getImg():
    username = request.form.get('username')
    imgurl = query_db_outside(query['selectUserImg'], (username,))
    if (imgurl):
        return jsonify({'code': 200, 'meaasge': 'ok', 'data': imgurl[0]['imgpath']})
    else:
        return jsonify({'code': 300, 'meaasge': 'ok', 'data': ''})

@user.route('/logout', methods=['POST'])
def logout():
    sessionid = request.form.get('sessionid')
    if(sessionid):
        redis.delete(sessionid)
        return jsonify({'code': 200, 'meaasge': 'ok', 'data': ''})

@user.route('/getHeadImgByUserid', methods=['POST'])
def getHeadImgByUserid():
    sessionid = request.form.get('sessionid')
    if redis.get(sessionid) is None:
        return jsonify({'code': 401, 'meaasge': 'No This User', 'data': ''})
    if redis.get(sessionid) is not None:
        userid = redis.get(sessionid).decode()
        imgurl = query_db_outside(query['selectUserImgByUserid'], (userid,))
        return jsonify({'code': 200, 'meaasge': 'ok', 'data': imgurl[0]['imgpath']})

@user.route('/checkSession', methods=['POST'])
def check():
    sessionid = request.form.get('sessionid')
    if (sessionid):
        if redis.get(sessionid) is not None:
            return jsonify({'code': 200, 'meaasge': 'ok', 'data': ''})
        else :
            return jsonify({'code': 401, 'meaasge': 'No this User', 'data': ''})
    else :
        return jsonify({'code': 401, 'meaasge': 'No this User', 'data': ''})