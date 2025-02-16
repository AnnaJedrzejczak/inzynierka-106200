from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Wczytanie klucza API z pliku .env
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Lista słów kluczowych związanych z filmami
FILM_KEYWORDS = ["film", "kino", "aktor", "reżyser", "scenariusz", "gatunek", "Oscar", "serial", "seans", "adaptacja", "ekranizacja", "produkcja", "animacja"]

@app.route("/")  # Ładuje stronę główną
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])  # Obsługuje zapytania użytkownika i wysyła je do ChatGPT.
def chat():
    user_message = request.json.get("message", "").strip().lower()

    # Sprawdzenie, czy pytanie użytkownika dotyczy filmów
    if not any(keyword in user_message for keyword in FILM_KEYWORDS):
        return jsonify({"reply": "Przepraszam, ale mogę rozmawiać tylko o filmach. Zadaj pytanie związane z kinematografią!"})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś ekspertem od filmów. Możesz odpowiadać TYLKO na pytania związane z filmami, aktorami, reżyserami, scenariuszami i gatunkami filmowymi. Jeśli użytkownik zapyta o coś spoza tej tematyki, grzecznie odmów odpowiedzi."},
                {"role": "user", "content": user_message}
            ]
        )

        return jsonify({"reply": response["choices"][0]["message"]["content"]})

    except Exception as e:
        return jsonify({"reply": f"Błąd: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
