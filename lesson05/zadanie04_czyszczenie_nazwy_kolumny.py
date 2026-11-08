# Lekcja 05 - Zadanie 4: Czyszczenie nazwy kolumny

# Dane wejściowe
raw_col = " Customer ID "

# Czyszczenie nazwy kolumny
clean_col = raw_col.strip().lower().replace(" ", "_")

# Wyświetlanie wyników
print(f"Oryginalna nazwa: '{raw_col}'")
print(f"Oczyszczona nazwa: '{clean_col}'")
