# Lekcja 10 - Zadanie 1: Tworzenie i analiza tablic

import numpy as np


# Tworzenie tablicy liczb od 1 do 100
liczby = np.arange(1, 101)

# Obliczenia statystyczne
suma = np.sum(liczby)
srednia = np.mean(liczby)
mediana = np.median(liczby)
minimum = np.min(liczby)
maksimum = np.max(liczby)

# Wyswietlenie wynikow
print("TWORZENIE I ANALIZA TABLIC NUMPY")
print("=" * 60)

print(f"Tablica: {liczby}")
print(f"Liczba elementow: {liczby.size}")

print("\nSTATYSTYKI")
print("=" * 60)

print(f"Suma: {suma}")
print(f"Srednia: {srednia:.2f}")
print(f"Mediana: {mediana:.2f}")
print(f"Minimum: {minimum}")
print(f"Maksimum: {maksimum}")

# Weryfikacja wynikow
print("\nWERYFIKACJA")
print("=" * 60)

print(f"Czy tablica ma 100 elementow: {liczby.size == 100}")
print(f"Czy suma jest poprawna: {suma == 5050}")
print(f"Czy srednia jest poprawna: {srednia == 50.5}")
print(f"Czy mediana jest poprawna: {mediana == 50.5}")
print(f"Czy minimum wynosi 1: {minimum == 1}")
print(f"Czy maksimum wynosi 100: {maksimum == 100}")
