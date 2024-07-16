from flask import Flask, request, jsonify, session
from flask_session import Session

app = Flask(__name__)

app.secret_key = 'mySecretKey123'

app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

data_store = []


@app.route('/login', methods=['POST'])
def login():
    user_data = request.json
    session['user'] = user_data['username']
    return jsonify({"message": "Logged in"}), 200


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out"}), 200


# @app.route('/data', methods=['GET'])
# def get_data():
#     if 'user' not in session:
#         return jsonify({"error": "Unauthorized"}), 401
#     return jsonify(data_store)


@app.route('/do-math', methods=['POST'])
def do_math():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    new_data = request.json
    data_store.append(new_data)
    return jsonify(new_data), 201


if __name__ == '__main__':
    app.run(debug=True)
