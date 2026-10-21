import os
from dotenv import load_dotenv
from certifi import contents
from google import genai
from google.genai import types

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL="gemini-3.8-flash"

SYSTEM=(
    "Jesteś asystentem pracowników banku. Odpowiadaj wyłącznie na podstawie podanego "
    "fragmentu regulaminu. Jeśli odpowiedzi nie ma we fragmencie, napisz 'Nie znalazłem tego "
    "w dostępnych dokumentach'"
)

KONTEKST=(
        "Dzienny limit przelewów wynosi 10 000 zł. Infolinia banku działa od poniedziałku do piątku w godzinach 8:00–18:00. "
        "Bank rozpatruje reklamacje w ciągu 14 dni roboczych. Z usług banku mogą korzystać tylko osoby pełnoletnie. "
        "Konto jest bezpłatne przy wpływach powyżej 2000 zł miesięcznie. Zgubioną lub skradzioną kartę należy natychmiast zablokować w aplikacji. "
        "Sesja w bankowości internetowej wygasa po 5 minutach braku aktywności. Rozwiązanie umowy o konto wymaga miesięcznego okresu wypowiedzenia."
        )

def zapytaj(pytanie):
    response=client.models.generate_content(
        model=MODEL,
        contents=f"FRAGMENT:\n{KONTEKST}\n\nPYTANIE: {pytanie}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            temperature=0
        ),
    )
    return response.text

import time
from google.genai import errors

def zapytaj_z_ponowieniem(pytanie, proby=5):
    for i in range(proby):
        try:
            return zapytaj(pytanie)
        except errors.APIError as e:
            if e.code in (429, 503) and i < proby - 1:
                time.sleep(2 ** i)
            else:
                raise

