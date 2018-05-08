import sys
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, flash, redirect
import os

file = Blueprint('file', __name__)

UPLOAD_FOLDER = sys.path[0] + '/static/uploads'
ALLOWED_EXTENSIONS = set(['sql'])

@file.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    f = request.files['testfile']
    print(f.filename)
    print(f)
    print(request.files)
    return jsonify({'code': 200})

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 上传任务文件
@file.route('/add', methods=['GET', 'POST'])
def uploadfile():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'data': '/static/uploads' + filename})
  return 'fail';

# 删除上传的任务文件
@file.route('/remove', methods=['GET', 'POST'])
def removefile():
  filepath = request.form.get('filename', default='')
  os.remove(os.path.join(UPLOAD_FOLDER, filepath))
  return 'remove success'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d