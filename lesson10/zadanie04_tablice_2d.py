# Lekcja 10 - Zadanie 4: Tablice 2D

import numpy as np


# Ustawienie ziarna losowania
np.random.seed(0)

# Tablica 5x4 z liczbami od 1 do 50
tablica = np.random.randint(1, 51, size=(5, 4))

# Odczyt danych z tablicy
ksztalt = tablica.shape
drugi_wiersz = tablica[1, :]
trzecia_kolumna = tablica[:, 2]
element_2_3 = tablica[2, 3]

print("TABLICE DWUWYMIAROWE NUMPY")
print("=" * 65)

print("Tablica 5x4:")
print(tablica)

print("\nKSZTALT TABLICY")
print("=" * 65)
print(f"Shape: {ksztalt}")

print("\nDRUGI WIERSZ")
print("=" * 65)
print(drugi_wiersz)

print("\nTRZECIA KOLUMNA")
print("=" * 65)
print(trzecia_kolumna)

print("\nELEMENT Z POZYCJI (2, 3)")
print("=" * 65)
print(f"tablica[2, 3] = {element_2_3}")

print("\nWERYFIKACJA")
print("=" * 65)

print(f"Czy tablica ma ksztalt (5, 4): {ksztalt == (5, 4)}")
print(f"Czy tablica ma 20 elementow: {tablica.size == 20}")
print(f"Czy wszystkie liczby sa od 1 do 50: {np.all((tablica >= 1) & (tablica <= 50))}")
print(f"Czy drugi wiersz ma 4 elementy: {drugi_wiersz.size == 4}")
print(f"Czy trzecia kolumna ma 5 elementow: {trzecia_kolumna.size == 5}")
print(f"Czy element (2, 3) jest poprawny: {element_2_3 == tablica[2][3]}")
