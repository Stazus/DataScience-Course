# Lekcja 07 - Zadanie 20: Min-Max normalizacja

# Dane wejsciowe
dane = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# 1. Inicjalizacja minimum i maksimum
mn = dane[0]
mx = dane[0]

# Wyznaczenie minimum i maksimum bez min() i max()
for x in dane:
    if x < mn:
        mn = x

    if x > mx:
        mx = x

# 2. Normalizacja Min-Max - list comprehension
znorm = [(x - mn) / (mx - mn) for x in dane]

# 3. Wyswietlenie wynikow
print("NORMALIZACJA MIN-MAX")
print("=" * 50)

print(f"Dane oryginalne: {dane}")
print(f"Minimum: {mn}")
print(f"Maksimum: {mx}")

print(f"\nDane znormalizowane: {znorm}")

# Weryfikacja wynikow
print("\nWERYFIKACJA")
print(f"Pierwsza wartosc: {znorm[0]}")
print(f"Ostatnia wartosc: {znorm[-1]}")
print(f"Czy pierwsza wartosc wynosi 0.0: {znorm[0] == 0.0}")
print(f"Czy ostatnia wartosc wynosi 1.0: {znorm[-1] == 1.0}")
