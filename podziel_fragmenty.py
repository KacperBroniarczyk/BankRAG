import json
import random

PLIK_PDF = "Regulamin-kont-dla-klientow-indywidualnych-od-06.07.2026.pdf"
ROZMIAR = 800       # maksymalna długość fragmentu w znakach
NAKLADANIE = 100    # ile znaków ostatniego fragmentu powtarzamy w następnym


def podziel_na_fragmenty(tekst, rozmiar=ROZMIAR, nakladanie=NAKLADANIE):
    if rozmiar <= nakladanie * 2:
        raise ValueError("rozmiar musi być większy niż 2 * nakladanie")

    tekst = tekst.strip()
    fragmenty = []
    start = 0

    while start < len(tekst):
        koniec = min(start + rozmiar, len(tekst))
        if koniec < len(tekst):
            spacja = tekst.rfind(" ", start + rozmiar // 2, koniec)
            if spacja != -1:
                koniec = spacja

        fragment = tekst[start:koniec].strip()
        if fragment:
            fragmenty.append(fragment)
        if koniec >= len(tekst):
            break
        start = koniec - nakladanie
        if start > 0 and tekst[start - 1] != " ":
            spacja = tekst.find(" ", start, koniec)
            if spacja != -1:
                start = spacja + 1

    return fragmenty


def podziel_strony(strony, zrodlo, rozmiar=ROZMIAR, nakladanie=NAKLADANIE):
    wynik = []
    numer = 1
    for strona in strony:
        for fragment in podziel_na_fragmenty(strona["tekst"], rozmiar, nakladanie):
            wynik.append({
                "id": numer,
                "zrodlo": zrodlo,
                "strona": strona["strona"],
                "tekst": fragment,
            })
            numer = numer + 1

    return wynik


def zapisz_json(dane, sciezka):
    with open(sciezka, "w", encoding="utf-8") as plik:
        json.dump(dane, plik, ensure_ascii=False, indent=2)


def pokaz_statystyki(fragmenty, ile_losowych=5):
    dlugosci = [len(f["tekst"]) for f in fragmenty]
    print("Liczba fragmentów:", len(fragmenty))
    print("Najkrótszy:", min(dlugosci))
    print("Najdłuższy:", max(dlugosci))
    print("Średnia:", round(sum(dlugosci) / len(dlugosci), 1))

    print("\nLosowe fragmenty do przeczytania:")
    for f in random.sample(fragmenty, min(ile_losowych, len(fragmenty))):
        print(f"\n[id {f['id']}, strona {f['strona']}, {len(f['tekst'])} znaków]")
        print(repr(f["tekst"]))


if __name__ == "__main__":
    from czyszczenie_pdf import wczytaj_strony, wyczysc_dokument

    teksty = wczytaj_strony(PLIK_PDF)
    strony, stale = wyczysc_dokument(teksty)

    fragmenty = podziel_strony(strony, PLIK_PDF)
    zapisz_json(fragmenty, "fragmenty.json")

    print("Liczba stron:", len(strony))
    pokaz_statystyki(fragmenty)