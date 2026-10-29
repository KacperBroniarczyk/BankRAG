import json
from pathlib import Path

from google.genai import types

from embedding import embed_pytanie, klient, normalizuj_wektory, szukaj, wczytaj_cache, z_ponawianiem

KATALOG = Path(__file__).parent
MODEL_GEN = "gemini-3.5-flash"
PROG = 0.6
K = 3
ODMOWA = "Nie znalazłem odpowiedzi na to pytanie w regulaminie."

SYSTEM = (
    "Jesteś asystentem pracownika banku. Odpowiadasz wyłącznie na podstawie "
    "podanych fragmentów regulaminu. Przy każdej informacji podaj numer strony "
    "w formacie (str. X). Jeśli fragmenty nie zawierają odpowiedzi, napisz dokładnie: "
    f"\"{ODMOWA}\" i nic więcej nie dodawaj. Odpowiadaj krótko i po polsku."
)


def wczytaj_indeks(sciezka_fragmentow=KATALOG / "fragmenty.json", sciezka_cache=KATALOG / "embeddingi.json"):
    with open(sciezka_fragmentow, "r", encoding="utf-8") as plik:
        fragmenty = json.load(plik)
    cache = wczytaj_cache(sciezka_cache)
    brakujace = [f["id"] for f in fragmenty if str(f["id"]) not in cache]
    if brakujace:
        raise ValueError(f"brak embeddingów dla {len(brakujace)} fragmentów, uruchom embedding.py")
    macierz = normalizuj_wektory([cache[str(f["id"])] for f in fragmenty])
    return fragmenty, macierz


def zbuduj_kontekst(trafienia, fragmenty):
    czesci = []
    for indeks, _ in trafienia:
        fragment = fragmenty[indeks]
        czesci.append(f"[strona {fragment['strona']}]\n{fragment['tekst']}")
    return "\n\n".join(czesci)


def zbuduj_prompt(pytanie, kontekst):
    return f"Fragmenty regulaminu:\n\n{kontekst}\n\nPytanie: {pytanie}"


def generuj_gemini(prompt):
    wynik = z_ponawianiem(
        lambda: klient().models.generate_content(
            model=MODEL_GEN,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM,
                temperature=0.1,
            ),
        )
    )
    return wynik.text or ODMOWA


def odpowiedz(pytanie, fragmenty, macierz, embed=embed_pytanie, generuj=generuj_gemini, prog=PROG, k=K):
    trafienia = szukaj(embed(pytanie), macierz, k)
    dobre = [(indeks, podobienstwo) for indeks, podobienstwo in trafienia if podobienstwo >= prog]

    if not dobre:
        return {"odpowiedz": ODMOWA, "zrodla": [], "trafienia": trafienia}

    tekst = generuj(zbuduj_prompt(pytanie, zbuduj_kontekst(dobre, fragmenty)))

    if tekst.strip() == ODMOWA:
        return {"odpowiedz": ODMOWA, "zrodla": [], "trafienia": trafienia}

    strony = list(dict.fromkeys(fragmenty[indeks]["strona"] for indeks, _ in dobre))
    return {"odpowiedz": tekst, "zrodla": strony, "trafienia": trafienia}


if __name__ == "__main__":
    fragmenty, macierz = wczytaj_indeks()
    print("Wczytano", len(fragmenty), "fragmentów. Pusta linia kończy.\n")

    while True:
        try:
            pytanie = input("Pytanie: ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not pytanie:
            break
        wynik = odpowiedz(pytanie, fragmenty, macierz)
        print("\n" + wynik["odpowiedz"])
        if wynik["zrodla"]:
            print("Źródła: strony", ", ".join(str(s) for s in wynik["zrodla"]))
        print("Podobieństwa:", [round(p, 3) for _, p in wynik["trafienia"]], "\n")
