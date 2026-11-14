# Lekcja 07 - Zadanie 6: Goraczka

temperatury = [36.5, 37.8, 36.2, 38.5, 36.9, 39.2, 37.0]

liczba_goraczek = 0

# Wyszukiwanie przypadkow goraczki
for temperatura in temperatury:
    if temperatura >= 38.0:
        print(f"Gorączka: {temperatura:.1f}°C")
        liczba_goraczek += 1

# Obliczenie odsetka przypadkow goraczki
liczba_pomiarow = len(temperatury)
odsetek = liczba_goraczek / liczba_pomiarow * 100

# Wyswietlenie podsumowania
print(f"\nLiczba pomiarow: {liczba_pomiarow}")
print(f"Liczba przypadkow goraczki: {liczba_goraczek}")
print(f"Odsetek przypadkow goraczki: {odsetek:.2f}%")
