import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from embedding import normalizuj_wektory, cosinus, szukaj   # zmień nazwę pliku na swoją

# --- DANE TESTOWE (2D, żeby dało się je narysować na kartce) ---
A = [3, 4]    # długość 5, po normalizacji [0.6, 0.8]
B = [1, 0]    # wzdłuż osi x
C = [0, 2]    # wzdłuż osi y
D = [1, 1]    # po przekątnej (45 stopni)

# --- normalizuj_wektory ---
W = normalizuj_wektory([A, B, C])
assert W.shape == (3, 2)
assert np.allclose(W[0], [0.6, 0.8])
assert np.allclose(W[1], [1.0, 0.0])
assert np.allclose(W[2], [0.0, 1.0])
assert np.allclose(np.linalg.norm(W, axis=1), 1.0)       # każdy wiersz ma długość 1

assert np.allclose(normalizuj_wektory([[5, 0]]), [[1, 0]])   # jeden wiersz

# wektor zerowy w środku macierzy MUSI dać błąd (Twój poprzedni kod tu nie rzucał)
for zle in ([[1, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0]]):
    try:
        normalizuj_wektory(zle)
        assert False, "powinien być ValueError dla " + str(zle)
    except ValueError:
        pass

# --- cosinus ---
assert abs(cosinus(B, C) - 0.0) < 1e-9                   # prostopadłe
assert abs(cosinus(B, [7, 0]) - 1.0) < 1e-9              # równoległe, różna długość
assert abs(cosinus(B, [-3, 0]) + 1.0) < 1e-9             # przeciwne
assert abs(cosinus(B, D) - 2 ** -0.5) < 1e-9             # 45 stopni = 0.7071...
assert abs(cosinus(A, [6, 8]) - 1.0) < 1e-9              # skalowanie nie zmienia cosinusa
assert isinstance(cosinus(B, D), float)

# --- szukaj ---
M = normalizuj_wektory([B, C, D, [-1, 0]])               # indeksy: 0=B, 1=C, 2=D, 3=przeciwny do B

# pytanie [2, 0] jest równoległe do B (indeks 0), 45 stopni od D (indeks 2)
wynik = szukaj([2, 0], M, k=3)                           # POJEDYNCZY wektor, nie lista
assert [i for i, _ in wynik] == [0, 2, 1]                # kolejność: B, D, C
assert abs(wynik[0][1] - 1.0) < 1e-9
assert abs(wynik[1][1] - 2 ** -0.5) < 1e-9
assert abs(wynik[2][1] - 0.0) < 1e-9
assert all(isinstance(i, int) and isinstance(s, float) for i, s in wynik)

# k większe niż liczba wierszy: nie psuje się, zwraca tyle ile jest
assert len(szukaj([2, 0], M, k=10)) == 4
# k = 1 zwraca jeden wynik
assert len(szukaj([2, 0], M, k=1)) == 1
# wyniki są malejące
s = [x for _, x in szukaj([1, 0.3], M, k=4)]
assert s == sorted(s, reverse=True)
# najgorszy wynik to wiersz przeciwny do pytania
assert szukaj([5, 0], M, k=4)[-1][0] == 3
# skala pytania nie zmienia wyniku (pytanie jest normalizowane wewnątrz)
assert [i for i, _ in szukaj([1, 0.3], M, 4)] == [i for i, _ in szukaj([100, 30], M, 4)]

print("Wszystkie testy rdzenia przeszły")