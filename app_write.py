from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.dhe3vud.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('write.html')

@app.route("/api/write", methods=["POST"])
def write_post():
    title_receive = request.form['title_give']
    contents_receive = request.form['contents_give']
    tag_receive = request.form['tag_give']
    emo_receive = request.form['emo_give']

    doc = {
        'title':title_receive,
        'contents':contents_receive,
        'tag':tag_receive,
        'emo': emo_receive
    }
    db.write.insert_one(doc)

    return jsonify({'msg': '등록 완료'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)