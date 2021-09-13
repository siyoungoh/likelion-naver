from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# STEP 02 : url 만들기


@app.route("/sample")
def sample():
    return "<p>Hello, sample!</p>"

# STEP 03-1 : html 파일 띄우기


@app.route("/news")
def news():
    return render_template("index.html")

# STEP 03-2 : json 띄우기


@app.route("/json")
def json():
    return jsonify({"message": "Hello, JSON!"})

# STEP 04 : json 형식으로 db의 뉴스데이터 보내주기


@app.route("/newsdb")
def get_news():
    # news_item = []

    my_ip = ' 서버 public ip'
    username = 'likelion'
    password = 'wearethefuture'
    db_name = 'likelion'  # likelion
    collection_name = 'navernews'  # navernews

    client = MongoClient(host=my_ip, port=27017,
                         username=username, password=password)
    db = client[db_name]
    collection = db[collection_name]  # unique key 설정할 collection

    news_item = list(collection.find({}, {'_id': False}))

    return jsonify({"news": news_item})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
