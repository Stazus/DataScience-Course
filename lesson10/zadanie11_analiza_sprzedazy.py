# Lekcja 10 - Zadanie 11: Analiza datasetu sprzedazy

import numpy as np


# Generowanie danych: 6 produktow, 28 dni
np.random.seed(3)
sales = np.random.randint(50, 200, size=(6, 28))

# Sprzedaz w pierwszym i ostatnim tygodniu
pierwszy_tydzien = np.sum(sales[:, :7], axis=1)
ostatni_tydzien = np.sum(sales[:, -7:], axis=1)

# Trend sprzedazy per produkt
trend = ostatni_tydzien - pierwszy_tydzien

# Laczna sprzedaz w poszczegolnych tygodniach
sprzedaz_tygodniowa = np.array([
    np.sum(sales[:, 0:7]),
    np.sum(sales[:, 7:14]),
    np.sum(sales[:, 14:21]),
    np.sum(sales[:, 21:28])
])

# Najlepszy tydzien
najlepszy_tydzien = np.argmax(sprzedaz_tygodniowa)
najlepsza_sprzedaz = sprzedaz_tygodniowa[najlepszy_tydzien]

# Laczna sprzedaz per produkt
sprzedaz_produktow = np.sum(sales, axis=1)

# Klasyfikacja trendu
kierunek_trendu = np.where(
    trend > 0,
    "WZROST",
    np.where(trend < 0, "SPADEK", "BEZ ZMIAN")
)


print("ANALIZA DATASETU SPRZEDAZY - NUMPY")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(sales)
print(f"Shape: {sales.shape}")
print(f"Liczba pomiarow: {sales.size}")

print("\nSPRZEDAZ W PIERWSZYM TYGODNIU")
print("=" * 75)
print(pierwszy_tydzien)

print("\nSPRZEDAZ W OSTATNIM TYGODNIU")
print("=" * 75)
print(ostatni_tydzien)

print("\nTREND SPRZEDAZY PER PRODUKT")
print("=" * 75)
print(f"Roznica: {trend}")
print(f"Kierunek: {kierunek_trendu}")

print("\nSPRZEDAZ TYGODNIOWA")
print("=" * 75)
print(f"Tydzien 1: {sprzedaz_tygodniowa[0]} szt.")
print(f"Tydzien 2: {sprzedaz_tygodniowa[1]} szt.")
print(f"Tydzien 3: {sprzedaz_tygodniowa[2]} szt.")
print(f"Tydzien 4: {sprzedaz_tygodniowa[3]} szt.")

print("\nNAJLEPSZY TYDZIEN")
print("=" * 75)
print(f"Indeks tygodnia: {najlepszy_tydzien}")
print(f"Numer tygodnia: {najlepszy_tydzien + 1}")
print(f"Laczna sprzedaz: {najlepsza_sprzedaz} szt.")

print("\nWYKRES SPRZEDAZY PER PRODUKT")
print("=" * 75)
print("Legenda: jeden znak █ = 100 sztuk")

# Petla tylko do rysowania tekstowych slupkow
for i, sprzedaz in enumerate(sprzedaz_produktow, start=1):
    slupek = "█" * (sprzedaz // 100)
    print(f"Produkt {i}: {slupek} {sprzedaz} szt.")

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Laczna sprzedaz: {np.sum(sales)} szt.")
print(f"Produkty ze wzrostem: {np.count_nonzero(trend > 0)}")
print(f"Produkty ze spadkiem: {np.count_nonzero(trend < 0)}")
print(f"Produkty bez zmian: {np.count_nonzero(trend == 0)}")

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy tablica ma ksztalt (6, 28): {sales.shape == (6, 28)}")

print(f"Czy obliczono 6 trendow: {trend.size == 6}")

print(f"Czy obliczono 4 tygodnie: {sprzedaz_tygodniowa.size == 4}")

print(f"Czy trendy sa poprawne: "
      f"{np.array_equal(trend, np.sum(sales[:, 21:28] - sales[:, 0:7], axis=1))}")

print(f"Czy najlepszy tydzien jest poprawny: "
      f"{najlepsza_sprzedaz == np.max(sprzedaz_tygodniowa)}")

print(f"Czy suma tygodni odpowiada calej sprzedazy: "
      f"{np.sum(sprzedaz_tygodniowa) == np.sum(sales)}")

print(f"Czy suma produktow odpowiada calej sprzedazy: "
      f"{np.sum(sprzedaz_produktow) == np.sum(sales)}")

print(f"Czy wszystkie wartosci sa od 50 do 199: "
      f"{np.all((sales >= 50) & (sales < 200))}")
