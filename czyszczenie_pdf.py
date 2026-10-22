import re
from collections import Counter
from pypdf import PdfReader

# Ustawienia
SCIEZKA_PDF = "Regulamin-kont-dla-klientow-indywidualnych-od-06.07.2026.pdf"
PROG = 0.5   # linia musi być na co najmniej 50% stron, żeby uznać ją za stałą
ILE = 2      # ile linii od góry i od dołu strony sprawdzamy (minimum 1)

# Wczytanie
def wczytaj_strony(plik):
    teksty = []
    odczyt = PdfReader(plik)

    for strona in odczyt.pages:
        tekst = strona.extract_text()
        if tekst is None:
            tekst = ""
        teksty.append(tekst)

    return teksty

# Funkcje pomocnicze
def normalizacja(linia):
    return re.sub(r"\d+", "", linia).strip()

def indeksy_strefy(linie, ile):
    niepuste = []
    for numer, linia in enumerate(linie):
        if linia.strip():
            niepuste.append(numer)

    poczatek = niepuste[:ile]
    koniec = niepuste[-ile:]
    return set(poczatek + koniec)

# Przebieg 1: liczenie (nic nie zmienia w tekście)
def znajdz_stale_linie(teksty, prog, ile):
    licznik = Counter()

    for tekst in teksty:
        linie = tekst.split("\n")
        unikalne = set()
        for numer in indeksy_strefy(linie, ile):
            znormalizowana = normalizacja(linie[numer])
            if znormalizowana != "":
                unikalne.add(znormalizowana)

        licznik.update(unikalne)

    minimum = prog * len(teksty)

    stale = set()
    for linia, ile_stron in licznik.items():
        if ile_stron >= minimum:
            stale.add(linia)

    return stale

# Przebieg 2: czyszczenie jednej strony
def usun_stale_linie(tekst, strefa, stale):
    wynik = []
    linie = tekst.split("\n")

    for numer, linia in enumerate(linie):
        if numer in strefa:
            znormalizowana = normalizacja(linia)
            if znormalizowana == "" or znormalizowana in stale:
                continue
        wynik.append(linia)

    return "\n".join(wynik)

def sklej_dzielone_wyrazy(tekst):
    return re.sub(r"(\w)-\n(\w)", r"\1\2", tekst)

def uporzadkuj_biale_znaki(tekst):
    return re.sub(r"\s+", " ", tekst).strip()

def wyczysc_strone(tekst, stale, ile):
    linie = tekst.split("\n")
    strefa = indeksy_strefy(linie, ile)

    tekst = usun_stale_linie(tekst, strefa, stale)
    tekst = sklej_dzielone_wyrazy(tekst)
    tekst = uporzadkuj_biale_znaki(tekst)
    return tekst

# Całość
def wyczysc_dokument(teksty, prog=PROG, ile=ILE):
    stale = znajdz_stale_linie(teksty, prog, ile)   # przebieg 1, raz na dokument

    strony = []
    for numer, tekst in enumerate(teksty, start=1):  # przebieg 2, strona po stronie
        oczyszczony = wyczysc_strone(tekst, stale, ile)
        strony.append({"strona": numer, "tekst": oczyszczony})

    return strony, stale

if __name__ == "__main__":
    teksty = wczytaj_strony(SCIEZKA_PDF)
    strony, stale = wyczysc_dokument(teksty)
    print("Liczba stron:", len(teksty))
    print("Stałe linie:", sorted(stale))
    print("\nPRZED:", repr(teksty[1][:300]))
    print("PO:   ", repr(strony[1]["tekst"][:300]))