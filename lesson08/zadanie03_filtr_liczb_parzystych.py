# Lekcja 08 - Zadanie 03: Filtr liczb parzystych

# Zakres liczb od 1 do 100
liczby = range(1, 101)

# Filtrowanie liczb parzystych - list comprehension
parzyste = [x for x in liczby if x % 2 == 0]

# Wyswietlenie wynikow
print("FILTR LICZB PARZYSTYCH")
print("=" * 50)

print(f"Wszystkie liczby parzyste: {parzyste}")
print(f"\nPierwsze 10 liczb parzystych: {parzyste[:10]}")
print(f"Liczba elementow: {len(parzyste)}")

# Weryfikacja liczby elementow
print(f"Czy lista zawiera 50 elementow: {len(parzyste) == 50}")
