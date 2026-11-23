# Lekcja 10 - Zadanie 5: Statystyki per wiersz i kolumna

import numpy as np


# Generowanie danych sprzedazowych
np.random.seed(1)
sales = np.random.randint(10, 100, size=(4, 7))

# Obliczenia statystyczne
srednia_produkt = np.mean(sales, axis=1)
srednia_dzien = np.mean(sales, axis=0)

laczna_sprzedaz_dzien = np.sum(sales, axis=0)

najlepszy_dzien = np.argmax(laczna_sprzedaz_dzien)
najslabszy_produkt = np.argmin(srednia_produkt)


print("STATYSTYKI SPRZEDAZY - NUMPY")
print("=" * 70)

print("Tablica sprzedazy (4 produkty, 7 dni):")
print(sales)

print("\nSREDNIA SPRZEDAZ PER PRODUKT")
print("=" * 70)

for i, srednia in enumerate(srednia_produkt, start=1):
    print(f"Produkt {i}: {srednia:.2f}")

print("\nSREDNIA SPRZEDAZ PER DZIEN")
print("=" * 70)

for i, srednia in enumerate(srednia_dzien, start=1):
    print(f"Dzien {i}: {srednia:.2f}")

print("\nLACZNA SPRZEDAZ PER DZIEN")
print("=" * 70)
print(laczna_sprzedaz_dzien)

print("\nNAJLEPSZY DZIEN SPRZEDAZY")
print("=" * 70)

print(f"Dzien: {najlepszy_dzien + 1}")
print(f"Sprzedaz: {laczna_sprzedaz_dzien[najlepszy_dzien]}")

print("\nPRODUKT Z NAJNIZSZA SREDNIA SPRZEDAZA")
print("=" * 70)

print(f"Produkt: {najslabszy_produkt + 1}")
print(f"Srednia: {srednia_produkt[najslabszy_produkt]:.2f}")

print("\nWERYFIKACJA")
print("=" * 70)

print(f"Czy tablica ma ksztalt (4, 7): {sales.shape == (4, 7)}")
print(f"Czy obliczono 4 srednie produktow: {srednia_produkt.size == 4}")
print(f"Czy obliczono 7 srednich dziennych: {srednia_dzien.size == 7}")
print(f"Czy najlepszy dzien jest poprawny: {laczna_sprzedaz_dzien[najlepszy_dzien] == np.max(laczna_sprzedaz_dzien)}")
print(f"Czy najslabszy produkt jest poprawny: {srednia_produkt[najslabszy_produkt] == np.min(srednia_produkt)}")
print(f"Czy srednie sa spojne: {np.isclose(np.mean(srednia_produkt), np.mean(srednia_dzien))}")
