from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- 
from core_logic import DigitalLegacy, AvatarSimulator

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # <--- 

# This will act as our simple, in-memory "blockchain" database
digital_wills_db = {}

@app.route('/')
def index():
    """A simple welcome route to check if the server is running."""
    return "Mindsurance: Digital Legacy Protocol API is running!"

@app.route('/mint', methods=['POST'])
def mint_digital_will():
    """
    API endpoint to create and 'mint' a new digital will.
    Expects a JSON payload with 'user_id' and 'rules'.
    """
    data = request.get_json()
    if not data or 'user_id' not in data or 'rules' not in data:
        return jsonify({"error": "Invalid request. 'user_id' and 'rules' are required."}), 400

    user_id = data['user_id']
    rules = data['rules']

    try:
        legacy = DigitalLegacy(user_id=user_id, rules=rules)
        will_data = legacy.get_will_data()
        transaction_id = will_data['transaction_id']
        digital_wills_db[transaction_id] = will_data
        
        return jsonify({
            "message": "Digital Will successfully minted!",
            "transaction_id": transaction_id
        }), 201

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/chat', methods=['POST'])
def chat_with_avatar():
    """
    API endpoint to interact with an AI avatar.
    Expects a JSON payload with 'transaction_id' and 'query'.
    """
    data = request.get_json()
    if not data or 'transaction_id' not in data or 'query' not in data:
        return jsonify({"error": "Invalid request. 'transaction_id' and 'query' are required."}), 400
    
    transaction_id = data['transaction_id']
    user_query = data['query']

    will_data = digital_wills_db.get(transaction_id)
    if not will_data:
        return jsonify({"error": "Transaction ID not found. The digital will does not exist."}), 404

    try:
        avatar = AvatarSimulator(will_data)
        response = avatar.get_response(user_query)
        return jsonify({
            "user_query": user_query,
            "avatar_response": response
        }), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)