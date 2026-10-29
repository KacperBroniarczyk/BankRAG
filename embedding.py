import json
import os
import time

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

MODEL_EMB = "gemini-embedding-001"
WYMIAR = 768
_klient = None


def normalizuj_wektory(wektory):
    macierz = np.array(wektory, dtype=float)
    dlugosci = np.linalg.norm(macierz, axis=1, keepdims=True)
    if np.any(dlugosci == 0):
        raise ValueError("wektor zerowy nie ma kierunku")
    return macierz / dlugosci


def cosinus(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def szukaj(wektor_pytania, macierz, k=3):
    wektor = normalizuj_wektory([wektor_pytania])[0]
    podobienstwa = macierz @ wektor
    najlepsze = np.argsort(podobienstwa)[::-1]
    pierwsze_k = najlepsze[:k]
    return [(int(indeks), float(podobienstwa[indeks])) for indeks in pierwsze_k]


def wczytaj_cache(sciezka):
    if not os.path.exists(sciezka):
        return {}
    with open(sciezka, "r", encoding="utf-8") as f:
        return json.load(f)


def zapisz_cache(cache, sciezka):
    with open(sciezka, "w", encoding="utf-8") as f:
        json.dump(cache, f)


def policz_embeddingi(fragmenty, embed_funkcja, sciezka_cache, rozmiar_paczki=20, przerwa_s=1.0):
    cache = wczytaj_cache(sciezka_cache)
    do_zrobienia = []
    for fragment in fragmenty:
        if str(fragment["id"]) not in cache:
            do_zrobienia.append(fragment)

    for i in range(0, len(do_zrobienia), rozmiar_paczki):
        paczka = do_zrobienia[i : i + rozmiar_paczki]
        teksty = [f["tekst"] for f in paczka]
        wektory = embed_funkcja(teksty)
        if len(wektory) != len(paczka):
            raise ValueError(f"Oczekiwano {len(paczka)} wektorów, zamiast {len(wektory)}")
        for fragment, wektor in zip(paczka, wektory):
            cache[str(fragment["id"])] = list(wektor)
        zapisz_cache(cache, sciezka_cache)
        time.sleep(przerwa_s)

    return cache


def klient():
    global _klient
    if _klient is None:
        try:
            import truststore

            truststore.inject_into_ssl()
        except ImportError:
            pass
        load_dotenv()
        if os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").lower() == "true":
            _klient = genai.Client(
                vertexai=True,
                project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                location=os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west3"),
            )
        else:
            _klient = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _klient


def z_ponawianiem(wywolanie, proby=5):
    for i in range(proby):
        try:
            return wywolanie()
        except errors.APIError as e:
            if e.code == 503 and i < proby - 1:
                time.sleep(2**i)
            else:
                raise


def _embed(teksty, task_type, proby=5):
    wynik = z_ponawianiem(
        lambda: klient().models.embed_content(
            model=MODEL_EMB,
            contents=teksty,
            config=types.EmbedContentConfig(task_type=task_type, output_dimensionality=WYMIAR),
        ),
        proby,
    )
    return [e.values for e in wynik.embeddings]


def embed_dokumenty(teksty):
    return _embed(teksty, "RETRIEVAL_DOCUMENT")


def embed_pytanie(pytanie):
    return _embed([pytanie], "RETRIEVAL_QUERY")[0]


if __name__ == "__main__":
    with open("fragmenty.json", "r", encoding="utf-8") as f:
        fragmenty = json.load(f)

    cache = policz_embeddingi(fragmenty, embed_dokumenty, "embeddingi.json", przerwa_s=15)

    macierz = normalizuj_wektory([cache[str(f["id"])] for f in fragmenty])
    print("Macierz:", macierz.shape)

    pytanie = "Kto może dysponować pieniędzmi na koncie?"
    for indeks, podobienstwo in szukaj(embed_pytanie(pytanie), macierz, k=3):
        f = fragmenty[indeks]
        print(round(podobienstwo, 3), "| strona", f["strona"], "|", f["tekst"][:])
