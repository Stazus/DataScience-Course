# Smart Dependency Manager - raport

Analizowany notebook: `lesson02_practice.ipynb`

## 1. Wykryte importy

- `matplotlib`
- `numpy`
- `pandas`

## 2. Zainstalowane pakiety

| Modul | Pakiet | Wersja | Status |
|---|---|---|---|
| matplotlib | matplotlib | 3.11.2 | Zainstalowany |
| numpy | numpy | 2.5.4 | Zainstalowany |
| pandas | pandas | 3.0.6 | Zainstalowany |

## 3. Kontrola konfliktow zaleznosci

**Status:** OK

**Szczegoly:** No broken requirements found.

## 4. Sugerowane alternatywy

### matplotlib -> plotext

Biblioteka do prostych wykresow w terminalu. Nie zastapi wszystkich funkcji Matplotlib.

### pandas -> polars

Alternatywa do przetwarzania danych tabelarycznych. Moze byc szybsza w wybranych operacjach.


## 5. Brakujace biblioteki

Nie wykryto brakujacych bibliotek.

## 6. Ograniczenia analizy

- Importy sa analizowane statycznie za pomoca AST.
- Importy dynamiczne moga nie zostac wykryte.
- Kontrola pip check dotyczy aktywnego srodowiska.
- Sugestie alternatyw wymagaja indywidualnej oceny.
