from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# import requests
# from bs4 import BeautifulSoup
#
# import certifi
# ca = certifi.where()

from pymongo import MongoClient
client = MongoClient('mongodb+srv://dajung:sparta@cluster0.nea13z3.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/join')
def join():
    return render_template('join.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


