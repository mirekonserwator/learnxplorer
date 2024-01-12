import os
from time import sleep
from packaging import version
from flask import Flask, request, jsonify
import openai
from openai import OpenAI
import functions

required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

if current_version < required_version:
    raise ValueError(f"Error: OpenAI version {openai.__version__} is less than the required version 1.1.1")
else:
    print("OpenAI version is compatible.")

app = Flask(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)

assistant_id = functions.create_assistant(client)

@app.route('/start', methods=['GET'])
def start_conversation():
    print("Starting a new conversation...")
    thread = client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")
    return jsonify({"thread_id": thread.id})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    thread_id = data.get('thread_id')
    user_input = data.get('message', '')

    if not thread_id:
        print("Error: Missing thread_id")
        return jsonify({"error": "Missing thread_id"}), 400

    print(f"Received message: {user_input} for thread ID: {thread_id}")

    # Add the user's message to the thread
    client.beta.threads.messages.create(thread_id=thread_id,
                                        role="user",
                                        content=user_input)

    # Zwiększenie limitu czasu na 60 sekund
    timeout_seconds = 60

    # Run the Assistant
    run = functions.create_run(client, thread_id, assistant_id)

    # Czekaj, aż run zostanie zakończony lub limit czasu upłynie
    functions.wait_for_run_completion(client, thread_id, run.id, timeout_seconds)

    # Pobierz i zwróć najnowszą wiadomość od asystenta
    response = functions.get_assistant_response(client, thread_id)

    print(f"Assistant response: {response}")  # Debugging line
    return jsonify({"response": response})

# Uruchom serwer
if __name__ == '__main__':
    app.run()


