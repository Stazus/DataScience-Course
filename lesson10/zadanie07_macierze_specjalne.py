# Lekcja 10 - Zadanie 7: Tworzenie macierzy specjalnych

import numpy as np


# Macierz 3x3 wypelniona zerami
macierz_zer = np.zeros((3, 3))

# Macierz 4x4 wypelniona jedynkami
macierz_jedynek = np.ones((4, 4))

# Macierz identycznosci 5x5
macierz_identycznosci = np.eye(5)

# Macierz 3x4 wypelniona liczba 7
macierz_siodemek = np.full((3, 4), 7)

# Wektor 10 rownoodleglych wartosci od 0 do 1
wektor = np.linspace(0, 1, 10)


print("TWORZENIE MACIERZY SPECJALNYCH")
print("=" * 70)

print("\nMACIERZ ZER 3x3")
print("=" * 70)
print(macierz_zer)
print(f"Shape: {macierz_zer.shape}")

print("\nMACIERZ JEDYNEK 4x4")
print("=" * 70)
print(macierz_jedynek)
print(f"Shape: {macierz_jedynek.shape}")

print("\nMACIERZ IDENTYCZNOSCI 5x5")
print("=" * 70)
print(macierz_identycznosci)
print(f"Shape: {macierz_identycznosci.shape}")

print("\nMACIERZ SIODEMEK 3x4")
print("=" * 70)
print(macierz_siodemek)
print(f"Shape: {macierz_siodemek.shape}")

print("\nWEKTOR 10 WARTOSCI OD 0 DO 1")
print("=" * 70)
print(np.round(wektor, 4))
print(f"Liczba elementow: {wektor.size}")

print("\nWERYFIKACJA")
print("=" * 70)

print(
    f"Czy macierz zer jest poprawna: "
    f"{macierz_zer.shape == (3, 3) and np.all(macierz_zer == 0)}"
)

print(
    f"Czy macierz jedynek jest poprawna: "
    f"{macierz_jedynek.shape == (4, 4) and np.all(macierz_jedynek == 1)}"
)

print(
    f"Czy macierz identycznosci jest poprawna: "
    f"{np.array_equal(macierz_identycznosci, np.diag([1] * 5))}"
)

print(
    f"Czy macierz siodemek jest poprawna: "
    f"{macierz_siodemek.shape == (3, 4) and np.all(macierz_siodemek == 7)}"
)

print(f"Czy wektor ma 10 elementow: {wektor.size == 10}")

print(
    f"Czy wektor zaczyna sie od 0 i konczy na 1: "
    f"{wektor[0] == 0 and wektor[-1] == 1}"
)

print(
    f"Czy wartosci sa rownoodlegle: "
    f"{np.allclose(np.diff(wektor), 1 / 9)}"
)
