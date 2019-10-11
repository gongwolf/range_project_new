from flask import Flask, request, abort, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import JSONWebSignatureSerializer as Serializer
from datetime import date
from writeToDisk import writeToDisk
from datetime import datetime
import json
from gevent.pywsgi import WSGIServer


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'

token_serializer = Serializer(app.config['SECRET_KEY'])

auth = HTTPTokenAuth('Bearer')

users = ['gqxwolf', 'Huiping', 'Cibils']
for user in users:
    token = token_serializer.dumps({'username': user}).decode('utf-8')
    print('*** token for {}: {}\n'.format(user, token))


@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = token_serializer.loads(token)
    except:  # noqa: E722
        return False
    if 'username' in data:
        g.user = data['username']
        return True
    return False


@app.route('/webhook', methods=['POST'])
@auth.login_required
def webhook():
    if request.method == 'POST':
        json_data = request.json
        print("recievied the data at -- {} -- from [{}]".format(datetime.now(), json_data['deviceEUI']))
        writeToDisk(json.dumps(json_data))
        return '', 200
    else:
        abort(400)

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
