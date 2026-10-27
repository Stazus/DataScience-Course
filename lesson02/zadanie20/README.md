# Zadanie 20 – Green Data Science Dashboard

Interaktywny dashboard do szacowania zużycia energii i śladu
węglowego związanego z pracą z notebookami Jupyter.

## Technologie

- Python
- Streamlit
- Plotly
- nbformat
- ReportLab

## Funkcjonalności

1. Wczytywanie notebooków Jupyter (.ipynb).
2. Wyświetlanie statystyk komórek notebooka.
3. Symulacja zużycia energii na podstawie mocy urządzenia,
   wykorzystania mocy i czasu pracy.
4. Szacowanie emisji CO2e.
5. Interaktywne wykresy typu gauge.
6. Porównanie scenariusza bazowego i zoptymalizowanego.
7. Sugestie optymalizacji na podstawie statycznej analizy kodu.
8. Eksport raportu do pliku PDF.

## Uruchomienie

Z katalogu lesson02:

```bash
python -m streamlit run zadanie20/app.py
