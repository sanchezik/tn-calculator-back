from flask import Flask, request, jsonify, session
from flask_session import Session

from src.service import math_controller, service_user
from src.util import config

app = Flask(__name__)

app.secret_key = config.APP_SESSION_SECRET

app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

data_store = []


@app.route('/login', methods=['POST'])
def login():
    form = dict(request.form)
    res = service_user.login(form)
    if res["errors"]:
        return jsonify(res), 404
    else:
        session['user'] = res["user"]
        return jsonify(res), 200


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out"}), 200


@app.route('/do-math', methods=['POST'])
def do_math():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    form = dict(request.form)
    res = math_controller.do_math(form, None)
    if res["errors"]:
        return jsonify(res), 409
    else:
        return jsonify(res), 200


if __name__ == '__main__':
    app.run()
