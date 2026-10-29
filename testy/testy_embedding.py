import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from embedding import normalizuj_wektory, cosinus, szukaj

A = [3, 4]
B = [1, 0]
C = [0, 2]
D = [1, 1]

W = normalizuj_wektory([A, B, C])
assert W.shape == (3, 2)
assert np.allclose(W[0], [0.6, 0.8])
assert np.allclose(W[1], [1.0, 0.0])
assert np.allclose(W[2], [0.0, 1.0])
assert np.allclose(np.linalg.norm(W, axis=1), 1.0)

assert np.allclose(normalizuj_wektory([[5, 0]]), [[1, 0]])

for zle in ([[1, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0]]):
    try:
        normalizuj_wektory(zle)
        assert False, "powinien być ValueError dla " + str(zle)
    except ValueError:
        pass

assert abs(cosinus(B, C) - 0.0) < 1e-9
assert abs(cosinus(B, [7, 0]) - 1.0) < 1e-9
assert abs(cosinus(B, [-3, 0]) + 1.0) < 1e-9
assert abs(cosinus(B, D) - 2 ** -0.5) < 1e-9
assert abs(cosinus(A, [6, 8]) - 1.0) < 1e-9
assert isinstance(cosinus(B, D), float)

M = normalizuj_wektory([B, C, D, [-1, 0]])

wynik = szukaj([2, 0], M, k=3)
assert [i for i, _ in wynik] == [0, 2, 1]
assert abs(wynik[0][1] - 1.0) < 1e-9
assert abs(wynik[1][1] - 2 ** -0.5) < 1e-9
assert abs(wynik[2][1] - 0.0) < 1e-9
assert all(isinstance(i, int) and isinstance(s, float) for i, s in wynik)

assert len(szukaj([2, 0], M, k=10)) == 4
assert len(szukaj([2, 0], M, k=1)) == 1
s = [x for _, x in szukaj([1, 0.3], M, k=4)]
assert s == sorted(s, reverse=True)
assert szukaj([5, 0], M, k=4)[-1][0] == 3
assert [i for i, _ in szukaj([1, 0.3], M, 4)] == [i for i, _ in szukaj([100, 30], M, 4)]

print("Wszystkie testy rdzenia przeszły")