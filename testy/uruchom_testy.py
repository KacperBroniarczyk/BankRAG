import subprocess
import sys
from pathlib import Path

# uruchamia po kolei wszystkie pliki testy_*.py z tego katalogu
katalog = Path(__file__).parent
bledy = 0

for plik in sorted(katalog.glob("testy_*.py")):
    print(f"--- {plik.name}", flush=True)
    wynik = subprocess.run([sys.executable, str(plik)])
    if wynik.returncode != 0:
        bledy += 1

print()
if bledy:
    print(f"Nie przeszło plików: {bledy}")
else:
    print("Wszystkie pliki testów przeszły")
sys.exit(1 if bledy else 0)
