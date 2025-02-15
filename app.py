from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Wczytanie klucza API z pliku .env
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")  # ładuje stronę główną
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"]) # obsługuje zapytania użytkownika i wysyła je do ChatGPT.
def chat():
    user_message = request.json.get("message")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Jesteś ekspertem od filmów. Odpowiadasz tylko na pytania dotyczące filmów."},
                  {"role": "user", "content": user_message}]
    )

    return jsonify({"reply": response["choices"][0]["message"]["content"]})

if __name__ == "__main__":
    app.run(debug=True)





