# Program Ambasadorów AI – propozycja

**Szkic do dyskusji.** Dokument nie opisuje stanu faktycznego w SGB, tylko propozycję opartą na typowym układzie takich programów. Pola oznaczone *(do ustalenia)* wymagają informacji z organizacji. Jeśli podobny program już istnieje, to jest propozycja jego rozwinięcia, a nie budowy od zera.

---

## Po co

Narzędzia AI trafiają do pracowników szybciej, niż powstają zasady ich używania. Powstają dwa przeciwne problemy naraz: część osób nie korzysta wcale, bo nie wie, od czego zacząć, a część korzysta w sposób ryzykowny, np. wkleja dane klientów do publicznych narzędzi.

Ambasador AI to osoba w komórce organizacyjnej, która jest pierwszym punktem kontaktu w obu sprawach: pomaga zacząć i mówi, czego nie wolno. Program nie jest szkoleniem jednorazowym, tylko siecią ludzi, która utrzymuje temat przy życiu między szkoleniami.

---

## Cele

| cel | miara | horyzont |
|---|---|---|
| Podnieść praktyczną umiejętność korzystania z AI | liczba osób, które zgłaszają regularne użycie w pracy | 6 miesięcy |
| Zebrać pomysły na zastosowania z całej organizacji | liczba zgłoszonych przypadków użycia | kwartalnie |
| Ograniczyć ryzykowne użycie | liczba zgłoszonych incydentów, wyniki krótkiej ankiety wiedzy | ciągle |
| Przyspieszyć wybór projektów do wdrożenia | liczba pomysłów, które przeszły do prototypu | kwartalnie |

Miary są dobrane tak, żeby dało się je zebrać bez dodatkowej biurokracji. Jeśli pomiar wymaga nowego systemu, prawdopodobnie jest zły.

---

## Kto to jest ambasador

**Profil:** osoba z komórki biznesowej, nie z IT. Zna swój proces, ma zaufanie zespołu, chce się uczyć. Nie musi umieć programować.

**Czego NIE robi:** nie jest wsparciem technicznym, nie zatwierdza narzędzi, nie odpowiada za zgodność z prawem. Te role zostają tam, gdzie są dziś.

**Co robi (ok. 2–4 godziny miesięcznie):**
- odpowiada na pytania „czy mogę tego użyć do…” i kieruje dalej, gdy sprawa wykracza poza zasady,
- zbiera od zespołu pomysły i problemy, które mogłaby rozwiązać AI,
- pokazuje na spotkaniu zespołu jeden konkretny przykład użycia miesięcznie,
- uczestniczy w comiesięcznym spotkaniu ambasadorów,
- zgłasza zaobserwowane ryzyka.

**Co dostaje:** dostęp do narzędzi wcześniej niż reszta, szkolenia, bezpośredni kontakt z zespołem prowadzącym temat AI, widoczność w organizacji.

---

## Jak wybrać pierwszą grupę

1. *(do ustalenia)* **Liczba:** proponuję zacząć od 8–12 osób, po jednej z kluczowych komórek. Mniej niż 6 nie tworzy sieci, więcej niż 15 utrudnia prowadzenie spotkań.
2. **Zgłoszenie dobrowolne**, za zgodą przełożonego (czas ambasadora to realny koszt dla zespołu).
3. **Różnorodność komórek** ważniejsza niż poziom zaawansowania. Jedna osoba z obsługi klienta jest cenniejsza niż trzy osoby z IT.
4. **Kryterium wstępne:** kandydat potrafi opisać jeden problem ze swojej codziennej pracy, który chciałby rozwiązać. To od razu daje listę przypadków użycia.

---

## Harmonogram pierwszych 90 dni

| tydzień | działanie | rezultat |
|---|---|---|
| 1–2 | Nabór i wybór ambasadorów | lista 8–12 osób z poparciem przełożonych |
| 3 | Warsztat startowy (pół dnia): co potrafi AI, czego nie potrafi, zasady bezpieczeństwa danych | wspólny poziom wiedzy, podpisane zasady |
| 4–6 | Każdy ambasador zbiera w swojej komórce 3 przypadki użycia | lista ok. 30 pomysłów |
| 7 | Przegląd pomysłów: ocena wartości i wykonalności | 3–5 wybranych do prototypu |
| 8–11 | Prototypy wybranych przypadków, ambasadorzy jako testerzy | działające demo |
| 12 | Prezentacja wyników, decyzja o kolejnej turze | raport, decyzja o skalowaniu |

Spotkanie ambasadorów co miesiąc, 60 minut: jeden przykład użycia, jedno nowe narzędzie, pytania.

---

## Zasady bezpiecznego użycia (szkielet do uzupełnienia przez compliance)

Ta część wymaga zatwierdzenia przez dział prawny i bezpieczeństwa. Poniżej szkielet, nie gotowe zasady.

**Nigdy:**
- dane osobowe klientów (imię, nazwisko, PESEL, numer rachunku, adres) w narzędziach publicznych,
- dane objęte tajemnicą bankową,
- dokumenty wewnętrzne oznaczone jako poufne,
- decyzje wobec klienta podejmowane na podstawie samej odpowiedzi AI.

**Zawsze:**
- weryfikacja odpowiedzi w źródle, zanim trafi do klienta lub do dokumentu,
- świadomość, że model może podać przekonująco brzmiącą nieprawdę,
- zgłoszenie błędu, który mógł mieć skutki.

**Do ustalenia z compliance:**
- *(które narzędzia są dopuszczone i w jakich wersjach)*
- *(jak oznaczać treści współtworzone z AI)*
- *(kto przyjmuje zgłoszenia incydentów)*

---

## Powiązanie z wymogami regulacyjnymi

Rozporządzenie UE o sztucznej inteligencji (AI Act) nakłada na podmioty korzystające z systemów AI obowiązek zapewnienia odpowiedniego poziomu kompetencji AI wśród osób, które się nimi zajmują. Program ambasadorów jest jednym ze sposobów realizacji tego obowiązku i daje przy okazji udokumentowany ślad działań szkoleniowych.

Aktualny stan przepisów i terminy obowiązków trzeba sprawdzić przed wdrożeniem, bo daty wejścia w życie poszczególnych przepisów były zmieniane.

---

## Ryzyka programu

| ryzyko | ograniczanie |
|---|---|
| Ambasador nie ma czasu, rola zostaje na papierze | zgoda przełożonego z góry, jasny limit godzin, widoczne rezultaty |
| Program zamienia się w cykl szkoleń bez efektów | każdy kwartał kończy się prototypem albo decyzją o rezygnacji |
| Ambasadorzy stają się nieformalnym wsparciem technicznym | jasno opisane, czego rola nie obejmuje |
| Entuzjazm wyprzedza zasady bezpieczeństwa | warsztat startowy zaczyna się od zasad, nie od narzędzi |
| Po pierwszej turze temat wygasa | rotacja części składu, nowe przypadki użycia co kwartał |

---

## Otwarte pytania

- [ ] czy podobny program już istnieje w SGB lub w Zrzeszeniu
- [ ] które narzędzia AI są dziś dopuszczone do użytku
- [ ] kto odpowiada za zgodność i bezpieczeństwo w tym obszarze
- [ ] jaka jest skala organizacji (liczba komórek, oddziałów) – od tego zależy liczebność grupy
- [ ] czy istnieje budżet na licencje i szkolenia
