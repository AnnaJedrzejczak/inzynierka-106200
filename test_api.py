import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Wczytanie zmiennych z pliku .env

openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Jakie są najlepsze filmy science fiction?"}]
    )
    print("Odpowiedź API:", response["choices"][0]["message"]["content"])
except Exception as e:
    print("Błąd:", e)
