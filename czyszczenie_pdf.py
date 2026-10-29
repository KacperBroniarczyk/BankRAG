import re
from collections import Counter
from pypdf import PdfReader

SCIEZKA_PDF = "Regulamin-kont-dla-klientow-indywidualnych-od-06.07.2026.pdf"
PROG = 0.5
ILE = 2

def wczytaj_strony(plik):
    teksty = []
    odczyt = PdfReader(plik)

    for strona in odczyt.pages:
        tekst = strona.extract_text()
        if tekst is None:
            tekst = ""
        teksty.append(tekst)

    return teksty

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

def wyczysc_dokument(teksty, prog=PROG, ile=ILE):
    stale = znajdz_stale_linie(teksty, prog, ile)

    strony = []
    for numer, tekst in enumerate(teksty, start=1):
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