from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for demonstration purposes
data_store = []


# GET method to retrieve all data
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_store)


# POST method to add new data
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json
    data_store.append(new_data)
    return jsonify(new_data), 201


if __name__ == '__main__':
    app.run(debug=True)
