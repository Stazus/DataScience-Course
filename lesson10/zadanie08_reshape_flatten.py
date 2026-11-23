# Lekcja 10 - Zadanie 8: Reshape i flatten

import numpy as np


# Tablica wejsciowa
arr = np.arange(1, 13)

# Zmiana ksztaltu tablicy
macierz_3x4 = arr.reshape(3, 4)
macierz_2x6 = arr.reshape(2, 6)
macierz_4x3 = arr.reshape(4, 3)

# Splaszczenie tablicy do 1D
splaszczona_flatten = macierz_3x4.flatten()
splaszczona_ravel = macierz_3x4.ravel()


print("RESHAPE I FLATTEN - NUMPY")
print("=" * 70)

print("\nTABLICA ORYGINALNA")
print("=" * 70)
print(arr)
print(f"Shape: {arr.shape}")

print("\nRESHAPE (3, 4)")
print("=" * 70)
print(macierz_3x4)
print(f"Shape: {macierz_3x4.shape}")

print("\nRESHAPE (2, 6)")
print("=" * 70)
print(macierz_2x6)
print(f"Shape: {macierz_2x6.shape}")

print("\nRESHAPE (4, 3)")
print("=" * 70)
print(macierz_4x3)
print(f"Shape: {macierz_4x3.shape}")

print("\nSPLASZCZENIE TABLICY")
print("=" * 70)
print(f"flatten(): {splaszczona_flatten}")
print(f"ravel():   {splaszczona_ravel}")

print("\nWSPOLDZIELENIE PAMIECI")
print("=" * 70)

print(
    f"flatten() wspoldzieli pamiec: "
    f"{np.shares_memory(macierz_3x4, splaszczona_flatten)}"
)

print(
    f"ravel() wspoldzieli pamiec: "
    f"{np.shares_memory(macierz_3x4, splaszczona_ravel)}"
)

# Test praktyczny na osobnej tablicy
tablica_testowa = arr.copy().reshape(3, 4)

kopia = tablica_testowa.flatten()
widok = tablica_testowa.ravel()

print("\nTEST FLATTEN - KOPIA")
print("=" * 70)

kopia[0] = 999

print(f"Pierwszy element kopii: {kopia[0]}")
print(f"Pierwszy element macierzy: {tablica_testowa[0, 0]}")

print("\nTEST RAVEL - VIEW")
print("=" * 70)

widok[0] = 888

print(f"Pierwszy element widoku: {widok[0]}")
print(f"Pierwszy element macierzy: {tablica_testowa[0, 0]}")

print("\nWERYFIKACJA")
print("=" * 70)

print(f"Czy reshape (3, 4) jest poprawny: {macierz_3x4.shape == (3, 4)}")
print(f"Czy reshape (2, 6) jest poprawny: {macierz_2x6.shape == (2, 6)}")
print(f"Czy reshape (4, 3) jest poprawny: {macierz_4x3.shape == (4, 3)}")

print(
    f"Czy flatten() zwraca poprawna tablice 1D: "
    f"{np.array_equal(splaszczona_flatten, arr)}"
)

print(
    f"Czy ravel() zwraca poprawna tablice 1D: "
    f"{np.array_equal(splaszczona_ravel, arr)}"
)

print(
    f"Czy flatten() tworzy kopie: "
    f"{not np.shares_memory(tablica_testowa, kopia)}"
)

print(
    f"Czy ravel() tworzy widok: "
    f"{np.shares_memory(tablica_testowa, widok)}"
)

print(f"Czy kopia pozostala niezalezna: {kopia[0] == 999}")
print(f"Czy zmiana widoku zmienila macierz: {tablica_testowa[0, 0] == 888}")

print(
    f"Czy dane oryginalne pozostaly niezmienione: "
    f"{np.array_equal(arr, np.arange(1, 13))}"
)
