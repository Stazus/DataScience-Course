# Lekcja 07 - Zadanie 13: Klasyfikacja KNN (1D, k=3)

# Dane treningowe
trening = [
    (1.5, 'A'),
    (2.3, 'A'),
    (3.8, 'B'),
    (4.2, 'B'),
    (5.1, 'B')
]

x_nowy = 3.5
k = 3

# 1. Obliczenie odleglosci od nowego punktu
odleglosci = [
    (abs(x_nowy - x), klasa)
    for x, klasa in trening
]

# 2. Sortowanie wedlug odleglosci
posortowane = sorted(odleglosci)

# 3. Wybor trzech najblizszych sasiadow
sasiedzi = posortowane[:k]

# 4. Zliczanie wystapien poszczegolnych klas
liczba_A = sum([1 for odleglosc, klasa in sasiedzi if klasa == 'A'])
liczba_B = sum([1 for odleglosc, klasa in sasiedzi if klasa == 'B'])

# 5. Klasyfikacja nowego punktu
if liczba_A > liczba_B:
    przewidywana_klasa = 'A'
else:
    przewidywana_klasa = 'B'

# Wyswietlenie wynikow
print("KLASYFIKACJA KNN")
print("=" * 50)
print(f"Nowy punkt: {x_nowy}")
print(f"Liczba sasiadow k: {k}")

print("\nTRZEJ NAJBLIZSI SASIEDZI")

for i, (odleglosc, klasa) in enumerate(sasiedzi, 1):
    print(f"{i}. Odleglosc: {odleglosc:.2f}, klasa: {klasa}")

print("\nPODSUMOWANIE")
print(f"Liczba glosow klasy A: {liczba_A}")
print(f"Liczba glosow klasy B: {liczba_B}")
print(f"Przewidywana klasa: {przewidywana_klasa}")
