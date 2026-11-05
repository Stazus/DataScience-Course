# Lekcja 04 - Zadanie 5: Parsing ścieżki pliku

sciezka = "data/processed/train_fold_03_normalized.csv"

# Podział ścieżki na foldery i nazwę pliku
elementy = sciezka.split("/")

folder = "/".join(elementy[:-1])
nazwa_pliku = elementy[-1]

# Oddzielenie rozszerzenia od nazwy pliku
czesci_pliku = nazwa_pliku.split(".")
format_pliku = czesci_pliku[-1]

# Wyodrębnienie informacji z nazwy pliku
czesci_nazwy = czesci_pliku[0].split("_")

typ_zbioru = czesci_nazwy[0]
numer_fold = czesci_nazwy[2]

# Wyświetlenie wyników
print(f"Folder: {folder}")
print(f"Typ zbioru: {typ_zbioru}")
print(f"Numer fold: {numer_fold}")
print(f"Format pliku: {format_pliku}")
