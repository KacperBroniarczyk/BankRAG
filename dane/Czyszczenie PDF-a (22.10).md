## Czyszczenie PDF-a (22.10)

### Dokument
- Plik: `Regulamin-kont-dla-klientow-indywidualnych-od-06.07.2026.pdf`, 40 stron.
- Źródło: `https://www.pgbs.pobiedziska.sgb.pl/wp-content/uploads/2026/05/Regulamin-kont-dla-klientow-indywidualnych-od-06.07.2026.pdf`, pobrany 21.10.
- PDF nie jest skanem: `extract_text()` zwraca tekst, polskie znaki są poprawne.

### Obserwacje w surowym tekście
- Na początku każdej strony pojawia się numer strony w osobnej linii.
- Reszta tekstu jest czytelna. Pozostałe niedoskonałości (np. układ) wynikają z samego dokumentu.
- Brak dzielonych wyrazów -\n. Brak wystąpień stopki. 

### Decyzje

| Data | Decyzja | Dlaczego | Alternatywy |
|---|---|---|---|
| 22.10 | Wykrywanie nagłówków i stopek przez liczenie linii z brzegów stron (po usunięciu cyfr) | Numer strony zmienia się co stronę, a reszta linii jest stała. Brzegi, bo zwykłe zdania rzadko powtarzają się na brzegu | Stała lista wzorców do usunięcia, ręczne czyszczenie |
| 22.10 | Dwa przebiegi: najpierw liczenie na całym dokumencie, potem czyszczenie strona po stronie | Jedna strona nie pokaże, co się powtarza w dokumencie | Jeden przebieg (nie da się ocenić powtórzeń) |
| 22.10 | `PROG = 0.5`, `ILE = 2` | Wartości startowe. Do zmiany po obejrzeniu brzegów stron. | Inne wartości, np. `PROG = 0.2` |
| 22.10 | Wszystkie białe znaki zamieniane na pojedynczą spację | Prostota, spójny tekst do dzielenia na fragmenty | Zachowanie akapitów (trudniejsze) |
| 22.10 | Numer strony zapisywany przy każdej oczyszczonej stronie | Pozwoli podać źródło odpowiedzi asystenta | Brak numeru (odpowiedź nie do zweryfikowania) |

### Wynik
- Wykrywanie stałych linii dla `PROG = 0.5`, `ILE = 2` zwróciło pustą listę. Numery stron są usuwane osobną regułą (linia pusta po usunięciu cyfr), więc nie trafiają do zbioru stałych linii.

### Ograniczenia
- Tabele zlewają się w jeden ciąg znaków.
- Podział na akapity jest tracony.
- Przy bardzo krótkich dokumentach (1-2 strony) próg uzna za stałe prawie każdą linię z brzegu.
- Nagłówki różne na stronach parzystych i nieparzystych mogą nie zostać wykryte.
- Skany wymagają OCR, którego program nie obsługuje.