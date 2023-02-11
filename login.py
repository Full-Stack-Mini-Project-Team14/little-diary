from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://dajung:sparta@cluster0.nea13z3.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbsparta

SECRET_KEY = 'SPARTA'

import jwt
import datetime
import hashlib

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('main.html', id=user_info["id"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/api/join', methods=['POST'])
def join_post():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    user_list = list(db.user.find({}, {'_id': False}))
    if id_receive == '' or pw_receive == '':
        return jsonify({'msg': '정보를 입력하세요.'})
    elif id_receive != '' and pw_receive != '':
        doc = {
            'id': id_receive,
            'pw': pw_hash,
        }
        db.user.insert_one(doc)

    id_str = str(id_receive)
    for i in user_list:
            if i['id'] == id_str:
                return jsonify({'msg': '중복된 id 입니다.'})
    return jsonify({'msg': '회원가입 완료.'})

    return jsonify({'result': 'success'})

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    doc = {
        'id': id_receive,
        'pw': pw_hash,
    }
    db.user.insert_one(doc)
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# @app.route('/api/nick', methods=['GET'])
# def api_valid():
#     token_receive = request.cookies.get('mytoken')
#
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         print(payload)
#         userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
#     return jsonify({'result': 'success', 'nickname': userinfo['nick']})
#
# except jwt.ExpiredSignatureError:
# # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
# return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
#
# except jwt.exceptions.DecodeError:
# return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


