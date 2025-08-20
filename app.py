import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from core_logic import DigitalLegacy, AvatarSimulator

# 
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

digital_wills_db = {}

# --- ---

@app.route('/mint', methods=['POST'])
def mint_digital_will():
    data = request.get_json()
    if not data or 'user_id' not in data or 'rules' not in data:
        return jsonify({"error": "Invalid request"}), 400
    legacy = DigitalLegacy(user_id=data['user_id'], rules=data['rules'])
    will_data = legacy.get_will_data()
    transaction_id = will_data['transaction_id']
    digital_wills_db[transaction_id] = will_data
    return jsonify({"message": "Success", "transaction_id": transaction_id}), 201

@app.route('/chat', methods=['POST'])
def chat_with_avatar():
    data = request.get_json()
    if not data or 'transaction_id' not in data or 'query' not in data:
        return jsonify({"error": "Invalid request"}), 400
    will_data = digital_wills_db.get(data['transaction_id'])
    if not will_data:
        return jsonify({"error": "Transaction ID not found"}), 404
    avatar = AvatarSimulator(will_data)
    response = avatar.get_response(data['query'])
    return jsonify({"user_query": data['query'], "avatar_response": response}), 200

# ---  ---

@app.route('/')
def serve_index():
    """"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """
   
    """
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)