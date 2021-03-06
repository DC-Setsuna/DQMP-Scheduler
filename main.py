import uuid
from urllib import response

from flask import Flask, session, request, jsonify
from flask_apscheduler import APScheduler
from flask_redis import FlaskRedis
from redis import Redis

from Config import Config
from flask_cors import CORS

from db.query_db import query_db_outside
from task.task import task
from file.file import file
from board.board import board
from log.log import log
from user.sql import query
from user.user import user

app = Flask(__name__, static_url_path='')
scheduler = APScheduler()
redis_store = FlaskRedis(app)

# redis = Redis(app)
redis = Redis()

DATABASE = './db/taskDB.db'

def interval_job():
    print('date job')

# 用户登录
@app.route('/login', methods=['POST'])
def Login():
    username = request.form.get('username')
    password = request.form.get('password')

    userinfo = query_db_outside(query['selectUserInfo'], (username, password,))
    if (userinfo):
        sessionId = uuid.uuid1()
        # redis.set(sessionId, userinfo[0]['user_id'])
        redis.setex(sessionId, userinfo[0]['user_id'], 1*60*60)
        return jsonify({'code': 200, 'meaasge': 'Login Success', 'data': sessionId, 'userid': userinfo[0]['user_id']})
    else:
        return jsonify({'code': 300, 'meaasge': 'Login Fail', 'data': ''})

@app.route('/')
def index():

    return app.send_static_file('index.html')

app.register_blueprint(task, url_prefix='/task')

app.register_blueprint(file, url_prefix='/file')

app.register_blueprint(board, url_prefix='/board')

app.register_blueprint(log, url_prefix='/log')

app.register_blueprint(user, url_prefix='/user')

app.config.from_object(Config())
# it is also possible to enable the API directly
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
