# Lekcja 08 - Zadanie 01: Kalkulator statystyk

# Definicja funkcji
def statystyki(liczby):
    """Zwraca sume, srednia, minimum i maksimum."""
    suma = sum(liczby)
    srednia = round(suma / len(liczby), 2)
    minimum = min(liczby)
    maksimum = max(liczby)

    return suma, srednia, minimum, maksimum


# Dane wejsciowe
oceny = [3.5, 4.0, 5.0, 3.0, 4.5, 5.0, 4.0, 3.5]

# Wywolanie funkcji
wynik = statystyki(oceny)

# Rozpakowanie krotki
suma, srednia, minimum, maksimum = wynik

# Wyswietlenie wynikow
print("KALKULATOR STATYSTYK")
print("=" * 50)
print(f"Lista ocen: {oceny}")
print(f"Liczba ocen: {len(oceny)}")
print(f"Suma: {suma}")
print(f"Srednia: {srednia:.2f}")
print(f"Minimum: {minimum}")
print(f"Maksimum: {maksimum}")

print(f"\nZwrocona krotka: {wynik}")
print(f"Typ wyniku: {type(wynik).__name__}")
