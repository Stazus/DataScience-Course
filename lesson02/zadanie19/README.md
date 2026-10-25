# Zadanie 19 — Notebook Quality Checker

## Cel projektu

Celem zadania jest stworzenie narzędzia do automatycznej
oceny jakości notebooków Jupyter.

## Funkcjonalności

Program sprawdza:

1. Udział komórek Markdown i komentarzy (minimum 20%).
2. Występowanie poleceń magicznych Jupyter.
3. Ustawienia ziarna losowości (random seed).
4. Instrukcje zapisywania wykresów.
5. Dobre praktyki organizacji notebooka:
   - komórka Markdown na początku,
   - brak pustych komórek.
6. Złożoność kodu:
   - długość komórek,
   - poziom zagnieżdżenia instrukcji.
7. Complexity Score (0–100).
8. Quality Score (0–100).
9. Poprawność formatu i struktury notebooka.

## Uruchamianie

Program należy uruchamiać z katalogu lesson02.

Przykład:

python zadanie19/notebook_quality_checker.py zadanie19/test_good_notebook.ipynb

## Wymagane biblioteki

- nbformat
- IPython

Instalacja:

```bash
pip install nbformat ipython
```

Program wykorzystuje IPython do przekształcania
poleceń magicznych Jupyter na składnię Pythona,
co umożliwia ich analizowanie za pomocą modułu AST.

## Complexity Score

Początkowy wynik: 100 punktów.

- Komórka przekraczająca 30 niepustych linii: -10 punktów.
- Każdy poziom zagnieżdżenia powyżej 3: -5 punktów.

## Quality Score

Maksymalna liczba punktów: 100.

- Dokumentacja: 30 punktów.
- Markdown na początku: 15 punktów.
- Brak pustych komórek: 15 punktów.
- Złożoność kodu: maksymalnie 40 punktów.

## Wyniki testów

Notebook bez dokumentacji:
- Complexity Score: 100/100.
- Quality Score: 55/100.

Notebook z dokumentacją:
- Complexity Score: 100/100.
- Quality Score: 100/100.

## Obsługa błędów

Program wykrywa:
- nieistniejące pliki,
- nieprawidłowy JSON,
- błędy struktury notebooka,
- brak identyfikatorów komórek.

## Ograniczenia

Wykrywanie poleceń magicznych, ustawień random seed
i zapisywania wykresów opiera się na wyszukiwaniu tekstu.

Quality Score jest autorską, uproszczoną punktacją,
a nie oficjalnym standardem jakości notebooków.
