# Zadanie 18 – Multi-environment tester

## 1. Porównanie środowisk

| Środowisko | Python | Czas wykonania |
|---|---|---:|
| Local Python 3.9 | 3.9.25 | 2.757 s |
| Local Python 3.11 | 3.11.16 | 2.031 s |
| Docker Python 3.11 | 3.11.17 | 3.835 s |
| Google Colab | 3.13.16 | 0.022 s |

## 2. Porównanie wyników obliczeń

- Local Python 3.9 vs Local Python 3.11: **IDENTYCZNE**
- Local Python 3.9 vs Docker Python 3.11: **IDENTYCZNE**
- Local Python 3.9 vs Google Colab: **IDENTYCZNE**

## 3. Uwagi

- Porównywane są wyniki obliczeń, bez informacji o środowisku.
- Local Python 3.9, Local Python 3.11 i Docker: czas obejmuje uruchomienie procesu, kernela Jupyter oraz wykonanie notebooka.
- Google Colab: czas zmierzono wewnątrz notebooka za pomocą time.perf_counter().
- Czasy Google Colab i pozostałych środowisk nie są bezpośrednio porównywalne.
- Testy lokalne i Docker uruchamiane są automatycznie.
- Google Colab uruchamiany jest ręcznie, a zapisane wyniki są automatycznie porównywane.
- Wyniki czasu mogą zależeć od obciążenia komputera.
