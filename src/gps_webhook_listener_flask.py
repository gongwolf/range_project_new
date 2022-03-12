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
from pathlib import Path
from datetime import date

#from statistics_dir\MCPCalculation.py import mcp_without_date, mcp_with_date
#from statistics_dir\record_count.py import record_count_with_date, record_count

if platform == "linux":
    home_folder = "/home/gqxwolf/mydata/range_project_new"
elif platform == "win32":
    home_folder = 'C:/range_project_new'

sys.path.append(os.path.join(home_folder, 'statistics'))
sys.path.append(os.path.join(home_folder, 'statistics', 'MCP'))

from record_count import record_count_with_date, record_count
from MCPCalculation import mcp_without_date, mcp_with_date

logging.basicConfig(filename="gps_getting_server.log")

app = Flask(__name__)
app.config["SECRET_KEY"] = "top secret!"
app.logger.setLevel(logging.INFO)

token_serializer = Serializer(app.config["SECRET_KEY"])

############################################
auth = HTTPTokenAuth("Bearer")

users = ["gqxwolf", "Huiping", "Cibils"]
for user in users:
    token = token_serializer.dumps({"username": user}).decode("utf-8")
    print("*** token for {}: {}".format(user, token))
############################################

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
        try:
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
        except:
            error_folder = ''
            if platform == "linux":
                error_folder = './logs/error'
            elif platform == "win32":
                # error_folder = 'Z:\Abeeway\logs\error'
                error_folder = 'C:/range_project_new/logs/error'
            error_p = Path(error_folder)
            if not error_p.exists():
                error_p.mkdir()
            today_error_log_file = date.today().__str__().replace("-", "_") + "_data_receiving_error.log"
            p_error_log_file = error_p / today_error_log_file
            with p_error_log_file.open("a") as f:
                e = sys.exc_info()
                # print("Error: {} ".format(e))
                # print("Error data : {}".format(json_data))
                # print("============================================")
                f.write("Error while receiving the data at -- {} -- from [{}]".format(datetime.now(), json_data["deviceEUI"]))
                f.write("Error: {} \n".format(e))
                f.write("Error data : {}\n".format(json_data))
                f.write("============================================\n")
            abort(400)
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


@app.route("/api/vi/gps/mcp/refresh", methods=["GET"])
def call_mcp_refresh():
    if 'date' in request.args:
        date = request.args['date']
        if date == "today":
            date = datetime.now().strftime("%Y_%m_%d")
        result = mcp_with_date(date)
    else:
        result = mcp_without_date()

    str_result: str = ""
    for s in result:
        str_result += s + "\n"
    str_result += "The GPS MCP refresh finished !!!!!.\n"
    app.logger.info(str_result)

    web_result: str = ""
    for s in result:
        web_result += s + "<br>"
    web_result += "The GPS MCP refresh finished !!!!!.<br>"

    return web_result


if __name__ == "__main__":
    http_server = WSGIServer(("", 5000), app, log=app.logger)
    http_server.serve_forever()
