import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from embedding import normalizuj_wektory
from ocena import bledy_przy_progu, czy_spoza, hit_at_k, kalibruj_prog, oceny_pytania, wczytaj_pytania


def ocena(id, miejsce, podobienstwo=0.8, spoza=False):
    return {"id": id, "miejsce_pierwszego_trafienia": miejsce, "najlepsze_podobienstwo": podobienstwo, "spoza": spoza}


# --- hit_at_k ---
oceny = [ocena(1, 1), ocena(2, 3), ocena(3, None), ocena(4, 2)]
assert hit_at_k(oceny, 1) == 0.25
assert hit_at_k(oceny, 3) == 0.75
assert hit_at_k(oceny, 5) == 0.75
assert hit_at_k([], 1) is None

# --- czy_spoza: po typie, a nie po pustej liście stron ---
assert czy_spoza({"typ": "spoza"})
assert czy_spoza({"typ": "spoza-bankowe"})
assert not czy_spoza({"typ": "bezposrednie", "strony": []})

# --- kalibruj_prog: zbiory rozdzielone ---
w_dok = [ocena(1, 1, 0.80), ocena(2, 1, 0.70)]
spoza = [ocena(3, None, 0.55, True), ocena(4, None, 0.60, True)]
wynik = kalibruj_prog(w_dok, spoza)
assert wynik["rozdzielone"] is True
assert wynik["proponowany_prog"] == 0.65

# --- kalibruj_prog: zbiory się nakładają, brak propozycji ---
wynik = kalibruj_prog(w_dok, spoza + [ocena(5, None, 0.75, True)])
assert wynik["rozdzielone"] is False
assert wynik["proponowany_prog"] is None

# --- bledy_przy_progu ---
b = bledy_przy_progu(w_dok, spoza + [ocena(5, None, 0.75, True)], 0.72)
assert b["odrzucone_z_dokumentu"] == [2]
assert b["przepuszczone_spoza"] == [5]

# --- oceny_pytania: miejsce pierwszej poprawnej strony ---
fragmenty = [{"strona": 3}, {"strona": 7}, {"strona": 9}]
M = normalizuj_wektory([[1, 0], [0, 1], [1, 1]])
pytanie = {"id": 1, "typ": "bezposrednie", "pytanie": "?", "strony": [9]}
o = oceny_pytania(pytanie, [1, 0], fragmenty, M, max_k=3)
assert o["znalezione_strony"] == [3, 9, 7]
assert o["miejsce_pierwszego_trafienia"] == 2

# --- prawdziwy zbiór pytań: każde pytanie z dokumentu ma wpisane strony ---
pytania = wczytaj_pytania()
assert len(pytania) >= 15
for p in pytania:
    if not czy_spoza(p):
        assert p["strony"], f"pytanie {p['id']} nie ma wpisanych stron"
    else:
        assert p["strony"] == [], f"pytanie spoza {p['id']} nie powinno mieć stron"

print("Wszystkie testy oceny przeszły")
