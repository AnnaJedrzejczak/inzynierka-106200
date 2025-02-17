from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
from keywords import FILM_KEYWORDS  # Import listy słów kluczowych
import markdown # type: ignore

load_dotenv()  # Wczytanie klucza API z pliku .env
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")  # Strona główna
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])  # Obsługuje zapytania użytkownika i wysyła je do ChatGPT
def chat():
    user_message = request.json.get("message", "").strip().lower()

    # Sprawdzenie, czy pytanie użytkownika dotyczy filmów
    if not any(keyword in user_message for keyword in FILM_KEYWORDS):
        return jsonify({"reply": "Przepraszam, ale mogę rozmawiać tylko o filmach. Zadaj pytanie związane z kinem!"})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Jesteś ekspertem od filmów. Możesz odpowiadać TYLKO na pytania związane z filmami, aktorami, reżyserami, scenariuszami i gatunkami filmowymi. Jeśli użytkownik zapyta o coś spoza tej tematyki, grzecznie odmów odpowiedzi."},
                {"role": "user", "content": user_message}
            ]
        )

        # Zamiana pojedynczych nowych linii na podwójne, aby poprawnie formatować odpowiedzi
        chat_response = response["choices"][0]["message"]["content"].replace("\n", "\n\n")

        # Konwersja Markdown na HTML
        chat_response_html = markdown.markdown(chat_response)

        return jsonify({"reply": chat_response_html})

    except Exception as e:
        return jsonify({"reply": f"Błąd: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
