# Lekcja 08 - Zadanie 08: Map i filter

# Dane wejsciowe
liczby = [-5, 3, -2, 8, 0, -1, 7, 4, -9, 6]

# Filtrowanie liczb dodatnich
dodatnie = list(filter(lambda x: x > 0, liczby))

# Podwojenie liczb dodatnich
wynik = list(map(lambda x: x * 2, dodatnie))

# Wyswietlenie wynikow
print("MAP I FILTER")
print("=" * 50)

print(f"Lista oryginalna: {liczby}")
print(f"Liczby dodatnie: {dodatnie}")
print(f"Liczby dodatnie podwojone: {wynik}")

# Weryfikacja wyniku
oczekiwane = [6, 16, 14, 8, 12]

print(f"\nCzy wynik jest poprawny: {wynik == oczekiwane}")
