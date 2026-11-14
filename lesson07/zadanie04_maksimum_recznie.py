# Lekcja 07 - Zadanie 4: Maksimum recznie

wyniki = [78, 92, 65, 88, 95, 71, 85]

# Inicjalizacja maksimum pierwszym elementem listy
maksimum = wyniki[0]

# Wyszukiwanie najwiekszej wartosci
for wynik in wyniki:
    if wynik > maksimum:
        maksimum = wynik

# Wyswietlenie wyniku
print(f"Najwieksza wartosc: {maksimum}")
