import json
import time
from datetime import datetime

from asystent import odpowiedz, wczytaj_indeks

PYTANIA = [
    ("w regulaminie", "Kto może dysponować pieniędzmi na koncie?"),
    ("w regulaminie", "Czy mogę ustanowić pełnomocnika do rachunku?"),
    ("w regulaminie", "Jak mogę wypowiedzieć umowę rachunku?"),
    ("w regulaminie", "Co się dzieje z rachunkiem po śmierci posiadacza?"),
    ("spoza regulaminu", "Jaka będzie jutro pogoda w Poznaniu?"),
    ("spoza regulaminu", "Ile kosztuje bitcoin?"),
]

fragmenty, macierz = wczytaj_indeks()
wyniki = []

for typ, pytanie in PYTANIA:
    wynik = odpowiedz(pytanie, fragmenty, macierz)
    podobienstwa = [round(p, 3) for _, p in wynik["trafienia"]]
    trafione_strony = [fragmenty[i]["strona"] for i, _ in wynik["trafienia"]]

    print("=" * 70)
    print(f"[{typ}] {pytanie}")
    print("-" * 70)
    print(wynik["odpowiedz"])
    print("Źródła:", wynik["zrodla"])
    print("Top 3 strony:", trafione_strony, "| podobieństwa:", podobienstwa)

    wyniki.append({
        "typ": typ,
        "pytanie": pytanie,
        "odpowiedz": wynik["odpowiedz"],
        "zrodla": wynik["zrodla"],
        "top3_strony": trafione_strony,
        "podobienstwa": podobienstwa,
    })
    time.sleep(5)

nazwa = f"dane/sprawdzenie_{datetime.now():%Y%m%d_%H%M}.json"
with open(nazwa, "w", encoding="utf-8") as plik:
    json.dump(wyniki, plik, ensure_ascii=False, indent=2)
print("=" * 70)
print("Zapisano:", nazwa)
