from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS
import json
import random
import threading

app = Flask(__name__, template_folder="templates")
CORS(app)  # Enable CORS for all routes

lock = threading.Lock()
# Load responses from JSON file
def load_responses():
    try:
        with open("responses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save responses to JSON file
def save_responses(responses):
    with open("responses.json", "w") as file:
        json.dump(responses, file, indent=4)

# Chatbot logic: If unknown, ask user to teach it
def get_response(user_input, responses):
    user_input = user_input.lower()

    for key in responses:
        if key in user_input:
            return random.choice(responses[key])

    return "I don't know how to respond. Please type how I should reply."

# ✅ Serve the Frontend (index.html)
@app.route("/")
def home():
    return render_template("index.html")  # Ensure index.html is in 'templates' folder

# ✅ Chatbot API Endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower()

    responses = load_responses()
    chatbot_response = get_response(user_message, responses)

    return jsonify({"response": chatbot_response})

# ✅ Learning API - Save User Response
@app.route("/learn", methods=["POST"])
def learn():
    data = request.json
    user_input = data.get("user_input", "").lower()
    bot_reply = data.get("bot_reply", "")

    if not user_input or not bot_reply:
        return jsonify({"status": "error", "message": "Invalid input"})

    responses = load_responses()

    # Save response
    if user_input in responses:
        responses[user_input].append(bot_reply)  # Append to existing responses
    else:
        responses[user_input] = [bot_reply]  # Create new entry

    save_responses(responses)

    return jsonify({"status": "success", "message": "Thanks! I've learned something new."})

if __name__ == "__main__":
    app.run(debug=True)
