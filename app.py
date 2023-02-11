from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

# import certifi
# ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.5omi5fs.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/diary/write", methods=["POST"])
def write_post():
    title_receive = request.form['title_give']
    contents_receive = request.form['contents_give']
    tag_receive = request.form['tag_give']
    emo_receive = request.form['emo_give']

    doc = {
        'title': title_receive,
        'contents': contents_receive,
        'tag': tag_receive,
        'emo': emo_receive
    }
    db.write.insert_one(doc)

    return jsonify({'msg': '등록 완료'})


@app.route("/diary/post", methods=["GET"])
def diary_get():
    write_list = list(db.write.find({}, {'_id': False}))
    return jsonify({'write':write_list})





@app.route('/diary/login')
def login():
    return render_template('login.html')

@app.route('/diary')
def write():
    return render_template('write.html')

@app.route('/diary/join')
def join():
    return render_template('join.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)


