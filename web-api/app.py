from flask import Flask, request
from threading import Lock
import json
import copy
from datetime import datetime

app = Flask(__name__)
dataWifi = []
dataBle = []
lock = Lock()


@app.route('/')
def hello_world():
    print("root path request - OK")
    return 'OK'


@app.route('/add', methods=['POST'])
def add():
    timestamp = datetime.today().replace(microsecond=0)
    wifiJson = request.json["wifi"]
    bleJson = request.json["ble"]
    print(wifiJson)
    print(bleJson)
    for i in wifiJson:
        if len(dataWifi) > 1000:
            dataWifi.pop(0)
        i["timestamp"] = timestamp
        dataWifi.append(i)
    for i in bleJson:
        if len(dataWifi) > 1000:
            dataWifi.pop(0)
        i["timestamp"] = timestamp
        dataWifi.append(i)
    print("Request '/add', added {} + {} objects".format(len(wifiJson), len(bleJson)))
    return 'OK'


@app.route('/get', methods=['GET'])
def get():
    with lock:
        resWifi = copy.deepcopy(dataWifi)
        resBle = copy.deepcopy(dataBle)
        dataWifi.clear()
        dataBle.clear()
    print("Request '/get', returned {} + {} objects".format(len(resWifi), len(resBle)))
    return json.dumps({"wifi": resWifi, "ble": resBle}, default=str)


@app.route('/check', methods=['POST'])
def check():
    content = request.json
    print(content)
    return 'Done'


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
