# Zadanie 18 – Multi-environment tester

## Cel zadania

Uruchomienie tego samego notebooka Jupyter w różnych środowiskach, porównanie wyników obliczeń oraz czasu wykonania.

## Testowane środowiska

- Lokalny Python 3.9
- Lokalny Python 3.11
- Docker z Pythonem 3.11
- Google Colab

## Pliki projektu

- `zadanie18.py` – główny program testujący
- `create_notebook.py` – generator notebooka
- `test_notebook.ipynb` – notebook testowy
- `test_notebook_colab.ipynb` – notebook z zapisanymi wynikami Google Colab
- `Dockerfile` – konfiguracja obrazu Docker
- `raport_zadanie18.md` – raport porównawczy

## Wymagania

- Python 3.9 i Python 3.11 w oddzielnych środowiskach wirtualnych
- Pakiety `ipykernel`, `nbformat`, `nbclient` w obu środowiskach
- Docker
- Pakiet `nbformat` w środowisku uruchamiającym główny program

## Przygotowanie środowisk lokalnych

Do zarządzania wersjami Pythona i środowiskami wirtualnymi wykorzystano narzędzie `uv`.

Polecenia należy wykonywać z katalogu `lesson02`.

Instalacja wymaganych wersji Pythona:

```bash
uv python install 3.9 3.11
```

Utworzenie środowisk wirtualnych:

```bash
uv venv zadanie18/venv39 --python 3.9
uv venv zadanie18/venv311 --python 3.11
```

Instalacja bibliotek:

```bash
uv pip install --python zadanie18/venv39/bin/python ipykernel nbformat nbclient
uv pip install --python zadanie18/venv311/bin/python ipykernel nbformat nbclient
```

W środowisku uruchamiającym główny program również musi być zainstalowany pakiet `nbformat`.

Środowiska `venv39` i `venv311` nie są przesyłane do repozytorium GitHub. Należy utworzyć je samodzielnie według powyższej instrukcji.


## Uruchomienie

Polecenia należy wykonywać z katalogu `lesson02`.

Zbudowanie obrazu Docker:

```bash
docker build -t zadanie18-tester:python311 -f zadanie18/Dockerfile zadanie18
```

Uruchomienie testera:

```bash
python zadanie18/zadanie18.py
```

Program uruchamia notebook w dwóch lokalnych środowiskach Pythona oraz w Dockerze, a następnie odczytuje wyniki zapisane w notebooku Google Colab.

## Google Colab

Notebook należy uruchomić ręcznie w Google Colab, a następnie zapisać wykonany plik jako `test_notebook_colab.ipynb` w katalogu `zadanie18`.

Program nie uruchamia zdalnej sesji Google Colab automatycznie.

## Wyniki

Tester porównuje wyniki obliczeń między środowiskami i wskazuje wykryte różnice.

Raport jest zapisywany w pliku `raport_zadanie18.md`.

Czasy wykonania w środowiskach lokalnych i Dockerze obejmują uruchomienie procesu oraz kernela Jupyter. Czas Google Colab jest mierzony wewnątrz notebooka, dlatego nie jest bezpośrednio porównywalny z pozostałymi.
