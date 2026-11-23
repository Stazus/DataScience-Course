# Lekcja 10 - Zadanie 10: Broadcasting w praktyce

import numpy as np


# Oceny 5 studentow z 4 egzaminow
exams = np.array([
    [78, 85, 92, 88],
    [65, 72, 68, 70],
    [90, 88, 95, 92],
    [55, 60, 58, 62],
    [82, 79, 85, 80]
])

# Bonusy dla poszczegolnych egzaminow
bonusy = np.array([5, 10, 5, 10])

# Indywidualne mnozniki studentow
mnozniki = np.array([1.0, 1.1, 0.95, 1.15, 1.0])

# Etap 1 - broadcasting po kolumnach
wyniki_z_bonusem = exams + bonusy

# Zmiana ksztaltu mnoznikow z (5,) na (5, 1)
mnozniki_kolumna = mnozniki.reshape(-1, 1)

# Etap 2 - broadcasting po wierszach
wyniki_koncowe = wyniki_z_bonusem * mnozniki_kolumna


print("BROADCASTING W PRAKTYCE - NUMPY")
print("=" * 70)

print("\nOCENY ORYGINALNE")
print("=" * 70)
print(exams)
print(f"Shape: {exams.shape}")

print("\nBONUSY EGZAMINACYJNE")
print("=" * 70)
print(bonusy)
print(f"Shape: {bonusy.shape}")

print("\nWYNIKI PO DODANIU BONUSOW")
print("=" * 70)
print(wyniki_z_bonusem)

print("\nMNOZNIKI STUDENTOW")
print("=" * 70)
print(mnozniki_kolumna)
print(f"Shape: {mnozniki_kolumna.shape}")

print("\nWYNIKI KONCOWE")
print("=" * 70)
print(np.round(wyniki_koncowe, 2))
print(f"Shape: {wyniki_koncowe.shape}")

print("\nSREDNIE WYNIKI STUDENTOW")
print("=" * 70)

print("Przed przeksztalceniem:")
print(np.round(np.mean(exams, axis=1), 2))

print("Po przeksztalceniu:")
print(np.round(np.mean(wyniki_koncowe, axis=1), 2))


# Oczekiwane wyniki do weryfikacji
oczekiwane = np.array([
    [83.0, 95.0, 97.0, 98.0],
    [77.0, 90.2, 80.3, 88.0],
    [90.25, 93.1, 95.0, 96.9],
    [69.0, 80.5, 72.45, 82.8],
    [87.0, 89.0, 90.0, 90.0]
])

print("\nWERYFIKACJA")
print("=" * 70)

print(
    f"Czy tablica ma ksztalt (5, 4): "
    f"{exams.shape == (5, 4)}"
)

print(
    f"Czy bonusy maja ksztalt (4,): "
    f"{bonusy.shape == (4,)}"
)

print(
    f"Czy mnozniki maja ksztalt (5, 1): "
    f"{mnozniki_kolumna.shape == (5, 1)}"
)

print(
    f"Czy bonusy dodano poprawnie: "
    f"{np.allclose(wyniki_z_bonusem - exams, bonusy)}"
)

print(
    f"Czy zachowano ksztalt tablicy: "
    f"{wyniki_koncowe.shape == exams.shape}"
)

print(
    f"Czy wyniki koncowe sa poprawne: "
    f"{np.allclose(wyniki_koncowe, oczekiwane)}"
)

print(
    f"Czy dane oryginalne pozostaly niezmienione: "
    f"{np.array_equal(exams, [[78, 85, 92, 88], [65, 72, 68, 70], [90, 88, 95, 92], [55, 60, 58, 62], [82, 79, 85, 80]])}"
)
