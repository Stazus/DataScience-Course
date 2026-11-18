# Lekcja 08 - Zadanie 09: Funkcja normalizacji Min-Max

# Wariant A - klasyczna petla for
def normalize_minmax(dane):
    """Normalizuje dane za pomoca petli for."""
    minimum = min(dane)
    maksimum = max(dane)

    wynik = []

    for x in dane:
        wartosc = (x - minimum) / (maksimum - minimum)
        wynik.append(round(wartosc, 3))

    return wynik


# Wariant B - list comprehension
def normalize_minmax_comprehension(dane):
    """Normalizuje dane za pomoca list comprehension."""
    minimum = min(dane)
    maksimum = max(dane)

    return [
        round((x - minimum) / (maksimum - minimum), 3)
        for x in dane
    ]


# Dane wejsciowe
wynagrodzenia = [3500, 4200, 5800, 7200, 9500, 4800, 6100]

# Wywolanie obu funkcji
wynik_a = normalize_minmax(wynagrodzenia)
wynik_b = normalize_minmax_comprehension(wynagrodzenia)

# Wyswietlenie wynikow
print("NORMALIZACJA MIN-MAX")
print("=" * 50)

print(f"Dane oryginalne: {wynagrodzenia}")
print(f"Minimum: {min(wynagrodzenia)}")
print(f"Maksimum: {max(wynagrodzenia)}")

print("\nWariant A - petla for:")
print(wynik_a)

print("\nWariant B - list comprehension:")
print(wynik_b)

# Weryfikacja wynikow
print("\nWERYFIKACJA")
print("=" * 50)

print(f"Minimum po normalizacji: {min(wynik_a)}")
print(f"Maksimum po normalizacji: {max(wynik_a)}")
print(f"Czy oba warianty sa identyczne: {wynik_a == wynik_b}")
print(f"Czy minimum wynosi 0.0: {min(wynik_a) == 0.0}")
print(f"Czy maksimum wynosi 1.0: {max(wynik_a) == 1.0}")
