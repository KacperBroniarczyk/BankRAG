import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from podziel_fragmenty import podziel_na_fragmenty, podziel_strony

assert podziel_na_fragmenty("") == []
assert podziel_na_fragmenty("   ") == []
assert podziel_na_fragmenty("krótki tekst") == ["krótki tekst"]

t = "aaaa bbbb cccc dddd eeee ffff gggg hhhh iiii jjjj"
assert podziel_na_fragmenty(t, 20, 5) == [
    "aaaa bbbb cccc dddd",
    "dddd eeee ffff gggg",
    "gggg hhhh iiii jjjj",
]

t2 = " ".join(["slowo%02d" % i for i in range(30)])
fr = podziel_na_fragmenty(t2, 60, 15)
assert len(fr) == 6
assert all(len(f) <= 60 for f in fr)
assert set(" ".join(fr).split()) == set(t2.split())
for poprzedni, nastepny in zip(fr, fr[1:]):
    assert poprzedni.split()[-1] in nastepny.split()
assert fr[0].startswith("slowo00")
assert fr[-1].endswith("slowo29")

assert podziel_na_fragmenty("x" * 50, 20, 5) == ["x" * 20] * 3

assert podziel_na_fragmenty("ab " + "x" * 60, 20, 5)[0] == "ab " + "x" * 17
assert all(f != "" for f in podziel_na_fragmenty("ab " + "x" * 60, 20, 5))

try:
    podziel_na_fragmenty("abc", 10, 5)
    assert False, "powinien być ValueError"
except ValueError:
    pass

strony = [
    {"strona": 1, "tekst": "Konto jest bezpłatne."},
    {"strona": 2, "tekst": ""},
    {"strona": 3, "tekst": "Drugi tekst."},
]
assert podziel_strony(strony, "a.pdf", 800, 100) == [
    {"id": 1, "zrodlo": "a.pdf", "strona": 1, "tekst": "Konto jest bezpłatne."},
    {"id": 2, "zrodlo": "a.pdf", "strona": 3, "tekst": "Drugi tekst."},
]

dluga = " ".join(["slowo%02d" % i for i in range(30)])
dwie = [{"strona": 1, "tekst": dluga}, {"strona": 2, "tekst": dluga}]
wynik = podziel_strony(dwie, "b.pdf", 60, 15)
assert len(wynik) == 12
assert [f["id"] for f in wynik] == list(range(1, 13))
assert wynik[6]["tekst"].startswith("slowo00")

print("Wszystkie testy przeszły")
