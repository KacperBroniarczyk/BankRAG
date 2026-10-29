import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

from asystent import PROG, wczytaj_indeks
from embedding import embed_pytanie, szukaj, wczytaj_cache, zapisz_cache

KATALOG = Path(__file__).parent
PLIK_PYTAN = KATALOG / "pytania_testowe.json"
CACHE_PYTAN = KATALOG / "embeddingi_pytan.json"
PLIK_RAPORTU = KATALOG / "dane" / "ocena_wyszukiwania.json"
POZIOMY_K = (1, 3, 5)
PRZERWA_S = 1.0


def wczytaj_pytania(sciezka=PLIK_PYTAN):
    with open(sciezka, "r", encoding="utf-8") as plik:
        pytania = json.load(plik)

    identyfikatory = [p["id"] for p in pytania]
    if len(set(identyfikatory)) != len(identyfikatory):
        raise ValueError("id pytań muszą być unikalne")
    for p in pytania:
        if "pytanie" not in p or "strony" not in p or "typ" not in p:
            raise ValueError(f"pytanie {p.get('id')} nie ma pola 'pytanie', 'strony' lub 'typ'")
    return pytania


def czy_spoza(pytanie):
    return pytanie.get("typ", "").startswith("spoza")


def wektory_pytan(pytania, embed=embed_pytanie, sciezka_cache=CACHE_PYTAN, przerwa_s=PRZERWA_S):
    cache = wczytaj_cache(sciezka_cache)
    nowe = 0

    for p in pytania:
        if p["pytanie"] not in cache:
            cache[p["pytanie"]] = list(embed(p["pytanie"]))
            zapisz_cache(cache, sciezka_cache)
            nowe += 1
            time.sleep(przerwa_s)

    return cache, nowe


def oceny_pytania(pytanie, wektor, fragmenty, macierz, max_k=max(POZIOMY_K)):
    trafienia = szukaj(wektor, macierz, max_k)
    strony = [fragmenty[indeks]["strona"] for indeks, _ in trafienia]
    podobienstwa = [podobienstwo for _, podobienstwo in trafienia]

    oczekiwane = set(pytanie["strony"])
    miejsce = None
    for numer, strona in enumerate(strony, start=1):
        if strona in oczekiwane:
            miejsce = numer
            break

    return {
        "id": pytanie["id"],
        "typ": pytanie.get("typ", ""),
        "spoza": czy_spoza(pytanie),
        "pytanie": pytanie["pytanie"],
        "oczekiwane_strony": sorted(oczekiwane),
        "znalezione_strony": strony,
        "podobienstwa": [round(p, 4) for p in podobienstwa],
        "najlepsze_podobienstwo": round(podobienstwa[0], 4),
        "miejsce_pierwszego_trafienia": miejsce,
    }


def hit_at_k(oceny, k):
    if not oceny:
        return None
    trafione = sum(1 for o in oceny if o["miejsce_pierwszego_trafienia"] is not None
                   and o["miejsce_pierwszego_trafienia"] <= k)
    return trafione / len(oceny)


def kalibruj_prog(w_dokumencie, spoza):
    najlepsze_w = [o["najlepsze_podobienstwo"] for o in w_dokumencie]
    najlepsze_spoza = [o["najlepsze_podobienstwo"] for o in spoza]

    wynik = {
        "w_dokumencie_min": min(najlepsze_w) if najlepsze_w else None,
        "w_dokumencie_srednia": round(float(np.mean(najlepsze_w)), 4) if najlepsze_w else None,
        "spoza_max": max(najlepsze_spoza) if najlepsze_spoza else None,
        "spoza_srednia": round(float(np.mean(najlepsze_spoza)), 4) if najlepsze_spoza else None,
        "proponowany_prog": None,
        "rozdzielone": None,
    }

    if najlepsze_w and najlepsze_spoza:
        dol, gora = min(najlepsze_w), max(najlepsze_spoza)
        wynik["rozdzielone"] = bool(dol > gora)
        if dol > gora:
            wynik["proponowany_prog"] = round((dol + gora) / 2, 3)

    return wynik


def bledy_przy_progu(w_dokumencie, spoza, prog):
    odrzucone = [o["id"] for o in w_dokumencie if o["najlepsze_podobienstwo"] < prog]
    przepuszczone = [o["id"] for o in spoza if o["najlepsze_podobienstwo"] >= prog]
    return {"prog": prog, "odrzucone_z_dokumentu": odrzucone, "przepuszczone_spoza": przepuszczone}


def raport(oceny, pytania, prog=PROG):
    spoza = [o for o in oceny if o["spoza"]]
    w_dokumencie = [o for o in oceny if not o["spoza"] and o["oczekiwane_strony"]]
    bez_stron = [o for o in oceny if not o["spoza"] and not o["oczekiwane_strony"]]

    return {
        "liczba_pytan": len(oceny),
        "w_dokumencie": len(w_dokumencie),
        "spoza_dokumentu": len(spoza),
        "bez_wpisanych_stron": [o["id"] for o in bez_stron],
        "hit": {f"hit@{k}": hit_at_k(w_dokumencie, k) for k in POZIOMY_K},
        "prog": kalibruj_prog(w_dokumencie, spoza),
        "obecny_prog": bledy_przy_progu(w_dokumencie, spoza, prog),
        "nietrafione": [
            {"id": o["id"], "pytanie": o["pytanie"],
             "oczekiwane": o["oczekiwane_strony"], "znalezione": o["znalezione_strony"]}
            for o in w_dokumencie if o["miejsce_pierwszego_trafienia"] is None
        ],
        "szczegoly": oceny,
    }


def wypisz(wynik):
    print("=" * 72)
    print(f"Pytań: {wynik['liczba_pytan']} "
          f"(z dokumentu: {wynik['w_dokumencie']}, spoza: {wynik['spoza_dokumentu']})")
    if wynik["bez_wpisanych_stron"]:
        print(f"UWAGA: pytania bez wpisanych stron (pominięte w hit@k): "
              f"{wynik['bez_wpisanych_stron']}")
    print("-" * 72)
    for nazwa, wartosc in wynik["hit"].items():
        if wartosc is None:
            print(f"{nazwa}: brak pytań z dokumentu")
        else:
            print(f"{nazwa}: {wartosc:.1%}")

    prog = wynik["prog"]
    print("-" * 72)
    print("Kalibracja progu:")
    print(f"  pytania z dokumentu: min {prog['w_dokumencie_min']}, "
          f"średnia {prog['w_dokumencie_srednia']}")
    print(f"  pytania spoza:       max {prog['spoza_max']}, "
          f"średnia {prog['spoza_srednia']}")
    if prog["rozdzielone"]:
        print(f"  zbiory rozdzielone -> proponowany PROG = {prog['proponowany_prog']}")
    elif prog["rozdzielone"] is False:
        print("  UWAGA: zbiory się nakładają, żaden próg nie rozdzieli ich bezbłędnie")

    obecny = wynik["obecny_prog"]
    print(f"  przy obecnym PROG = {obecny['prog']}: "
          f"odrzucone z dokumentu {obecny['odrzucone_z_dokumentu']}, "
          f"przepuszczone spoza {obecny['przepuszczone_spoza']}")

    if wynik["nietrafione"]:
        print("-" * 72)
        print("Nietrafione pytania (poprawna strona poza top 5):")
        for n in wynik["nietrafione"]:
            print(f"  [{n['id']}] {n['pytanie']}")
            print(f"       oczekiwano {n['oczekiwane']}, znaleziono {n['znalezione']}")
    print("=" * 72)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Ocena wyszukiwania: hit@k i próg")
    parser.add_argument("--bez-api", action="store_true",
                        help="nie licz nowych embeddingów, użyj wyłącznie cache")
    args = parser.parse_args(argv)

    pytania = wczytaj_pytania()
    fragmenty, macierz = wczytaj_indeks()

    if args.bez_api:
        cache = wczytaj_cache(CACHE_PYTAN)
        brakujace = [p["id"] for p in pytania if p["pytanie"] not in cache]
        if brakujace:
            print(f"Brak embeddingów dla pytań: {brakujace}. "
                  f"Uruchom bez --bez-api.", file=sys.stderr)
            return 1
    else:
        cache, nowe = wektory_pytan(pytania)
        print(f"Embeddingi pytań: {len(pytania)} (nowych wywołań API: {nowe})")

    oceny = [oceny_pytania(p, cache[p["pytanie"]], fragmenty, macierz) for p in pytania]
    wynik = raport(oceny, pytania)
    wypisz(wynik)

    PLIK_RAPORTU.parent.mkdir(exist_ok=True)
    with open(PLIK_RAPORTU, "w", encoding="utf-8") as plik:
        json.dump(wynik, plik, ensure_ascii=False, indent=2)
    print("Raport zapisany:", PLIK_RAPORTU)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
