import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from asystent import ODMOWA, odpowiedz, wczytaj_indeks, zbuduj_kontekst, zbuduj_prompt
from embedding import normalizuj_wektory

FRAGMENTY = [
    {"id": 1, "strona": 5, "tekst": "Konto jest bezpłatne."},
    {"id": 2, "strona": 7, "tekst": "Reklamację rozpatrujemy w 15 dni."},
    {"id": 3, "strona": 7, "tekst": "Kartę zastrzegasz w aplikacji."},
]
M = normalizuj_wektory([[1, 0], [0, 1], [1, 1]])


def atrapa_embed(wektor):
    return lambda pytanie: wektor


wywolania = []


def atrapa_generuj(prompt):
    wywolania.append(prompt)
    return "Odpowiedź (str. 5)"


def generuj_odmowe(prompt):
    return ODMOWA


kontekst = zbuduj_kontekst([(0, 0.9), (2, 0.7)], FRAGMENTY)
assert kontekst == "[strona 5]\nKonto jest bezpłatne.\n\n[strona 7]\nKartę zastrzegasz w aplikacji."
prompt = zbuduj_prompt("Czy konto jest darmowe?", kontekst)
assert prompt.startswith("Fragmenty regulaminu:")
assert prompt.endswith("Pytanie: Czy konto jest darmowe?")

wywolania.clear()
wynik = odpowiedz("pogoda?", FRAGMENTY, M, embed=atrapa_embed([-1, -1]), generuj=atrapa_generuj, prog=0.5, k=3)
assert wynik["odpowiedz"] == ODMOWA
assert wynik["zrodla"] == []
assert len(wynik["trafienia"]) == 3
assert wywolania == []

wywolania.clear()
wynik = odpowiedz("konto?", FRAGMENTY, M, embed=atrapa_embed([1, 0]), generuj=atrapa_generuj, prog=0.5, k=3)
assert wynik["odpowiedz"] == "Odpowiedź (str. 5)"
assert wynik["zrodla"] == [5, 7]
assert len(wywolania) == 1
assert "Konto jest bezpłatne." in wywolania[0]
assert "Kartę zastrzegasz" in wywolania[0]
assert "Reklamację" not in wywolania[0]

wynik = odpowiedz("reklamacja?", FRAGMENTY, M, embed=atrapa_embed([0, 1]), generuj=atrapa_generuj, prog=0.5, k=3)
assert wynik["zrodla"] == [7]

wywolania.clear()
odpowiedz("konto?", FRAGMENTY, M, embed=atrapa_embed([1, 0]), generuj=atrapa_generuj, prog=0.5, k=1)
assert "Kartę zastrzegasz" not in wywolania[0]

wynik = odpowiedz("konto?", FRAGMENTY, M, embed=atrapa_embed([1, 0]), generuj=generuj_odmowe, prog=0.5, k=3)
assert wynik["odpowiedz"] == ODMOWA
assert wynik["zrodla"] == []

with tempfile.TemporaryDirectory() as katalog:
    plik_fragmentow = Path(katalog) / "fragmenty.json"
    plik_cache = Path(katalog) / "embeddingi.json"
    plik_fragmentow.write_text(json.dumps(FRAGMENTY), encoding="utf-8")

    plik_cache.write_text(json.dumps({"1": [1, 0], "2": [0, 1]}), encoding="utf-8")
    try:
        wczytaj_indeks(plik_fragmentow, plik_cache)
        assert False, "powinien być ValueError (brak embeddingu dla id 3)"
    except ValueError:
        pass

    plik_cache.write_text(json.dumps({"1": [1, 0], "2": [0, 1], "3": [2, 2]}), encoding="utf-8")
    fragmenty, macierz = wczytaj_indeks(plik_fragmentow, plik_cache)
    assert len(fragmenty) == 3
    assert macierz.shape == (3, 2)

print("Wszystkie testy asystenta przeszły")
