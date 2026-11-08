# Lekcja 05 - Zadanie 8: Ekstrakcja informacji ze ścieżki

# Dane wejściowe
filename = "model_results_2024_Q3.csv"

# Podział nazwy pliku według podkreślników
elementy = filename.split("_")

# Wyodrębnienie roku
rok = elementy[2]

# Wyodrębnienie kwartału
kwartal = elementy[3].split(".")[0]

# Sprawdzenie rozszerzenia pliku
czy_csv = filename.endswith(".csv")

# Wyświetlanie wyników
print(f"Nazwa pliku: {filename}")
print(f"Rok: {rok}")
print(f"Kwartał: {kwartal}")
print(f"Czy plik CSV: {czy_csv}")
