# Lekcja 10 - Zadanie 3: Indeksowanie i slicing

import numpy as np


# Dane wejsciowe - temperatury
temps = np.array([15, 18, 22, 25, 23, 20, 17, 14, 16, 19, 21, 24])

# Indeksowanie i slicing
dni_parzyste = temps[::2]
ostatnie_piec = temps[-5:]
odwrotna_kolejnosc = temps[::-1]

# Filtrowanie warunkowe (Boolean indexing)
wieksze_niz_20 = temps[temps > 20]


print("INDEKSOWANIE I SLICING NUMPY")
print("=" * 65)

print(f"Temperatury: {temps}")
print(f"Liczba pomiarow: {temps.size}")

print("\nTEMPERATURY Z DNI PARZYSTYCH (INDEKSY 0, 2, 4...)")
print("=" * 65)
print(dni_parzyste)

print("\nOSTATNIE 5 TEMPERATUR")
print("=" * 65)
print(ostatnie_piec)

print("\nTEMPERATURY W ODWROTNEJ KOLEJNOSCI")
print("=" * 65)
print(odwrotna_kolejnosc)

print("\nTEMPERATURY WIEKSZE NIZ 20")
print("=" * 65)
print(wieksze_niz_20)


# Weryfikacja wynikow
print("\nWERYFIKACJA")
print("=" * 65)

print(
    f"Czy temperatury z indeksow parzystych sa poprawne: "
    f"{np.array_equal(dni_parzyste, [15, 22, 23, 17, 16, 21])}"
)

print(
    f"Czy ostatnie 5 temperatur jest poprawne: "
    f"{np.array_equal(ostatnie_piec, [14, 16, 19, 21, 24])}"
)

print(
    f"Czy odwrotna kolejnosc jest poprawna: "
    f"{np.array_equal(odwrotna_kolejnosc, temps[::-1])}"
)

print(
    f"Czy temperatury > 20 sa poprawne: "
    f"{np.array_equal(wieksze_niz_20, [22, 25, 23, 21, 24])}"
)
