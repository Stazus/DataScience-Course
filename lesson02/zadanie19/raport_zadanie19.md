# Raport — Zadanie 19
## Notebook Quality Checker

### 1. Cel zadania

Celem było opracowanie programu automatycznie
analizującego jakość notebooków Jupyter.

### 2. Zastosowane technologie

- Python 3.12
- nbformat
- ast
- json
- pathlib
- sys

### 3. Zrealizowane funkcjonalności

Program analizuje:

- udział komórek Markdown,
- udział komentarzy,
- polecenia magiczne Jupyter,
- ustawienia random seed,
- zapisywanie wykresów,
- strukturę notebooka,
- puste komórki,
- długość komórek kodu,
- poziom zagnieżdżenia instrukcji.

Na podstawie wyników oblicza:

- Complexity Score (0–100),
- Quality Score (0–100).

Program wyświetla również rekomendacje.

### 4. Wyniki testów

| Test | Wynik |
|---|---|
| Notebook bez dokumentacji | Quality Score: 55/100 |
| Notebook z dokumentacją | Quality Score: 100/100 |
| Brak pliku | Wykryto |
| Nieprawidłowy JSON | Wykryto |
| Brak ID komórki | Wykryto |
| Random seed | Wykryto random.seed(42) |
| Puste komórki w testowanych notebookach | Nie wykryto |

### 5. Analiza złożoności

Dla obu testowanych notebooków:

Complexity Score: 100/100.

Komórki nie przekraczały 30 niepustych linii,
a poziom zagnieżdżenia wynosił 0.

### 6. Wnioski

Program rozróżnia notebooki o różnym poziomie
dokumentacji i poprawnie oblicza Quality Score.

Wykrywa również wybrane błędy plików
oraz nieprawidłowości strukturalne.

### 7. Ograniczenia

- Niektóre kontrole wykorzystują wyszukiwanie tekstu.
- Punktacja jakości jest uproszczona.
- Nie przeprowadzono jeszcze testów automatycznych.
- Wykrywanie błędów struktury można dalej rozwijać.

### 8. Możliwe rozszerzenia

- Testy automatyczne pytest.
- Eksport raportu do JSON lub HTML.
- Analiza wielu notebooków jednocześnie.
- Rozbudowana analiza AST.
- Konfigurowalne progi punktacji.

### 9. Dodatkowe testy funkcjonalne

#### Test poleceń magicznych Jupyter

Plik: test_magic_notebook.ipynb

- Wykryto polecenie `%time`.
- Analiza AST z wykorzystaniem IPython zakończyła się poprawnie.
- Complexity Score: 100/100.
- Quality Score: 100/100.

#### Test głębokiego zagnieżdżenia

Plik: test_nested_notebook.ipynb

- Wykryto 4 poziomy zagnieżdżenia.
- Zastosowano karę 5 punktów.
- Complexity Score: 95/100.
- Quality Score: 98/100.

#### Test długości komórki

Plik: test_long_cell.ipynb

- Wykryto komórkę zawierającą 31 niepustych linii.
- Zastosowano karę 10 punktów.
- Complexity Score: 90/100.
- Quality Score: 96/100.

#### Test regresyjny

Po dodaniu obsługi IPython ponownie sprawdzono
test_good_notebook.ipynb.

- Complexity Score: 100/100.
- Quality Score: 100/100.

Wyniki potwierdziły prawidłowe działanie
sprawdzonych mechanizmów.
