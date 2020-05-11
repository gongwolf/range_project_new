import logging
from flask import Flask, request, abort, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import JSONWebSignatureSerializer as Serializer
from writeToDisk import writeToDisk
from datetime import datetime
import json
from gevent.pywsgi import WSGIServer
import sys
from sys import platform
import os

if platform == "linux":
    home_folder = "/home/gqxwolf/mydata/range_project_new"
elif platform == "win32":
    home_folder = 'C:\\range_project_new'

sys.path.append(os.path.join(home_folder, 'statistics'))

from record_count import record_count_with_date, record_count

logging.basicConfig(filename="gps_getting_server.log")

app = Flask(__name__)
app.config["SECRET_KEY"] = "top secret!"
app.logger.setLevel(logging.INFO)

token_serializer = Serializer(app.config["SECRET_KEY"])

auth = HTTPTokenAuth("Bearer")

users = ["gqxwolf", "Huiping", "Cibils"]
for user in users:
    token = token_serializer.dumps({"username": user}).decode("utf-8")
    print("*** token for {}: {}".format(user, token))


@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = token_serializer.loads(token)
    except:  # noqa: E722
        return False
    if "username" in data:
        g.user = data["username"]
        return True
    return False


@app.route("/webhook", methods=["POST"])
@auth.login_required
def webhook():
    if request.method == "POST":
        json_data = request.json
        print(
            "recievied the data at -- {} -- from [{}]".format(
                datetime.now(), json_data["deviceEUI"]
            )
        )
        app.logger.info(
            "recievied the data at -- {} -- from [{}]".format(
                datetime.now(), json_data["deviceEUI"]
            )
        )
        writeToDisk(json.dumps(json_data))
        return "", 200
    else:
        abort(400)


@app.route("/api/vi/gps/qualitycounts/refresh", methods=["GET"])
def call_gps_count_refresh():
    if 'date' in request.args:
        date = request.args['date']
        if date == "today":
            date = datetime.now().strftime("%Y_%m_%d")
        result = record_count_with_date(date)
    else:
        result = record_count()

    str_result: str = ""
    for s in result:
        str_result += s + "\n"
    str_result += "The GPS records refresh finished !!!!!.\n"
    app.logger.info(str_result)


    web_result: str = ""
    for s in result:
        web_result += s + "<br>"
    web_result += "The GPS records refresh finished !!!!!.<br>"

    return web_result


if __name__ == "__main__":
    http_server = WSGIServer(("", 5000), app, log=app.logger)
    http_server.serve_forever()
