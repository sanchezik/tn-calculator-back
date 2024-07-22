import time

from flask import Flask, request, jsonify, session, make_response
from flask_session import Session
from flask_cors import CORS

from src.service import math_controller, service_user
from src.util import config

app = Flask(__name__)

app.secret_key = config.APP_SESSION_SECRET

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
Session(app)
CORS(app)

data_store = []


@app.route('/login', methods=['POST'])
def action_login():
    form = dict(request.form)
    res = service_user.login(form)
    if res["errors"]:
        return jsonify(res), 404
    else:
        session['user'] = res["user"]
        session['limit'] = 20
        session['limit_renewal'] = time.time() + 60
        response = make_response(jsonify(res))
        response.headers.add('Access-Control-Allow-Origin', 'localhost')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.status_code = 200
        return response
        # return jsonify(res), 200


@app.route('/logout', methods=['POST'])
def action_logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out"}), 200


@app.route('/do-math', methods=['POST'])
def action_do_math():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    form = dict(request.form)
    res = math_controller.do_math(form, session)
    if res["errors"]:
        return jsonify(res), 409
    else:
        return jsonify(res), 200


@app.route('/my-records', methods=['POST'])
def action_my_records():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    form = dict(request.form)
    res = service_user.get_records(form, session["user"]["id"])
    if res["errors"]:
        return jsonify(res), 400
    else:
        return jsonify(res), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
