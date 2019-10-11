from flask import Flask, request, abort
from gevent.pywsgi import WSGIServer
import logging

logging.basicConfig(filename="log.log")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.logger.setLevel(logging.WARNING)


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        app.logger.info("it's a log :::   {}".format(request.json))
        return '', 200
    else:
        abort(400)


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app, log=app.logger)
    http_server.serve_forever()