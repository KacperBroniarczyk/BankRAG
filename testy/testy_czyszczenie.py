import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from czyszczenie_pdf import (
    normalizacja,
    indeksy_strefy,
    znajdz_stale_linie,
    usun_stale_linie,
    sklej_dzielone_wyrazy,
    uporzadkuj_biale_znaki,
    wyczysc_strone,
    wyczysc_dokument,
)

STRONY = [
    "1\nRegulamin\nTresc A\nTresc B\nStrona 1",
    "2\nRegulamin\nTresc C\nTresc D\nStrona 2",
    "3\nRegulamin\nTresc E\nTresc F\nStrona 3",
]
STALE = {"Regulamin", "Strona"}

assert normalizacja("Strona 12 z 40") == "Strona  z"
assert normalizacja("7") == ""
assert normalizacja("  Art. 5 ust. 2  ") == "Art.  ust."

assert indeksy_strefy(["a", "", "b", "c", "d"], 1) == {0, 4}
assert indeksy_strefy(["a", "b", "c"], 2) == {0, 1, 2}

assert znajdz_stale_linie(STRONY, 0.5, 2) == STALE

tekst = STRONY[0]
strefa = indeksy_strefy(tekst.split("\n"), 2)
assert usun_stale_linie(tekst, strefa, STALE) == "Tresc A\nTresc B"

assert sklej_dzielone_wyrazy("wpły-\nwach") == "wpływach"
assert sklej_dzielone_wyrazy("a - b") == "a - b"

assert uporzadkuj_biale_znaki("  Konto   jest\nbezpłatne \n") == "Konto jest bezpłatne"

assert wyczysc_strone(STRONY[0], STALE, 2) == "Tresc A Tresc B"

wynik, stale = wyczysc_dokument(STRONY, 0.5, 2)
assert stale == STALE
assert wynik[0] == {"strona": 1, "tekst": "Tresc A Tresc B"}
assert wynik[2] == {"strona": 3, "tekst": "Tresc E Tresc F"}

print("Wszystkie testy przeszły")