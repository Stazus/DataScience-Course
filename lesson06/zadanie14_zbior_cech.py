# Lekcja 06 - Zadanie 14: Zbior cech vs lista wartosci

# Dane datasetu Iris
dane = [
    ('setosa', 5.1, 3.5, 1.4, 0.2),
    ('setosa', 4.9, 3.0, 1.4, 0.2),
    ('versicolor', 7.0, 3.2, 4.7, 1.4),
    ('versicolor', 6.4, 3.2, 4.5, 1.5),
    ('virginica', 6.3, 3.3, 6.0, 2.5),
    ('virginica', 5.8, 2.7, 5.1, 1.9),
    ('setosa', 4.7, 3.2, 1.3, 0.2)
]

# Zbior unikalnych gatunkow
gatunki = {
    dane[0][0], dane[1][0], dane[2][0],
    dane[3][0], dane[4][0], dane[5][0],
    dane[6][0]
}

print(f"Unikalne gatunki: {gatunki}")
print(f"Liczba gatunkow: {len(gatunki)}")

# Pobranie i rozpakowanie pierwszego rekordu
pierwszy_rekord = dane[0]
gatunek, sl, sw, pl, pw = pierwszy_rekord

print("\nPIERWSZY REKORD")
print(f"Gatunek: {gatunek}")
print(f"Sepal length: {sl}")
print(f"Sepal width: {sw}")
print(f"Petal length: {pl}")
print(f"Petal width: {pw}")

# Lista dlugosci dzialek kielicha
sepal_length = [
    dane[0][1], dane[1][1], dane[2][1],
    dane[3][1], dane[4][1], dane[5][1],
    dane[6][1]
]

# Obliczenie statystyk
minimum = min(sepal_length)
maksimum = max(sepal_length)
suma = sum(sepal_length)
srednia = suma / len(sepal_length)

# Wyswietlenie wynikow
print("\nSTATYSTYKI SEPAL LENGTH")
print(f"Lista wartosci: {sepal_length}")
print(f"Minimum: {minimum:.3f}")
print(f"Maksimum: {maksimum:.3f}")
print(f"Suma: {suma:.3f}")
print(f"Srednia: {srednia:.3f}")
