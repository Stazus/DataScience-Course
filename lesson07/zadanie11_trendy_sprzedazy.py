# Lekcja 07 - Zadanie 11: Trendy sprzedazy

# Dane sprzedazy z 12 miesiecy
sprzedaz = [
    1200, 1350, 1290, 1480, 1520, 1510,
    1680, 1720, 1700, 1890, 1950, 2100
]

liczba_wzrostow = 0
liczba_spadkow = 0
suma_wzrostow = 0

print("MIESIACE ZE WZROSTEM SPRZEDAZY")
print("=" * 50)

# Porownanie kolejnych miesiecy
for i in range(1, len(sprzedaz)):
    poprzednia = sprzedaz[i - 1]
    aktualna = sprzedaz[i]

    zmiana = (aktualna - poprzednia) / poprzednia * 100

    if zmiana > 0:
        liczba_wzrostow += 1
        suma_wzrostow += zmiana

        print(
            f"Miesiac {i + 1}: wzrost z {poprzednia} "
            f"do {aktualna} ({zmiana:+.2f}%)"
        )

    elif zmiana < 0:
        liczba_spadkow += 1

# Obliczenie sredniego dodatniego wzrostu
sredni_wzrost = suma_wzrostow / liczba_wzrostow

# Podsumowanie
print("\nPODSUMOWANIE")
print("=" * 50)
print(f"Liczba miesiecy ze wzrostem: {liczba_wzrostow}")
print(f"Liczba miesiecy ze spadkiem: {liczba_spadkow}")
print(f"Sredni dodatni wzrost: {sredni_wzrost:.2f}%")
