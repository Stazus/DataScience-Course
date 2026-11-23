# Lekcja 10 - Zadanie 12: Odleglosc Euklidesowa

import numpy as np


def odleglosc_euklidesowa(a, b):
    return np.sqrt(np.sum((a - b) ** 2))


# Dwa punkty w przestrzeni 5-wymiarowej
point_a = np.array([1, 2, 3, 4, 5])
point_b = np.array([5, 4, 3, 2, 1])

# Obliczenie odleglosci pomiedzy punktami
roznica = point_a - point_b
kwadraty_roznic = roznica ** 2
suma_kwadratow = np.sum(kwadraty_roznic)

odleglosc = odleglosc_euklidesowa(point_a, point_b)

# Generowanie 4 punktow w przestrzeni 5-wymiarowej
np.random.seed(4)
points = np.random.rand(4, 5)

# Macierz roznic pomiedzy wszystkimi parami punktow
# Broadcasting: (4, 1, 5) - (1, 4, 5)
roznice = points[:, np.newaxis, :] - points[np.newaxis, :, :]

# Macierz odleglosci Euklidesowych
macierz_odleglosci = np.sqrt(
    np.sum(roznice ** 2, axis=2)
)

# Formatowanie tablic do 3 miejsc po przecinku
np.set_printoptions(precision=3, floatmode="fixed")


print("ODLEGLOSC EUKLIDESOWA - NUMPY")
print("=" * 75)

print("\nODLEGLOSC POMIEDZY DWOMA PUNKTAMI")
print("=" * 75)

print(f"Punkt A: {point_a}")
print(f"Punkt B: {point_b}")
print(f"Roznice: {roznica}")
print(f"Kwadraty roznic: {kwadraty_roznic}")
print(f"Suma kwadratow: {suma_kwadratow}")
print(f"Odleglosc Euklidesowa: {odleglosc:.3f}")

print("\nCZTERY PUNKTY W PRZESTRZENI 5D")
print("=" * 75)
print(points)
print(f"Shape: {points.shape}")

print("\nBROADCASTING - MACIERZ ROZNIC")
print("=" * 75)
print(f"Shape: {roznice.shape}")

print("\nMACIERZ ODLEGLOSCI EUKLIDESOWYCH")
print("=" * 75)
print(macierz_odleglosci)
print(f"Shape: {macierz_odleglosci.shape}")

print("\nPRZEKATNA MACIERZY")
print("=" * 75)
print(np.diag(macierz_odleglosci))

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy odleglosc A-B jest poprawna: "
      f"{np.isclose(odleglosc, np.sqrt(40))}")

print(f"Czy odleglosc A-B jest rowna B-A: "
      f"{np.isclose(odleglosc, odleglosc_euklidesowa(point_b, point_a))}")

print(f"Czy punkty maja ksztalt (4, 5): "
      f"{points.shape == (4, 5)}")

print(f"Czy macierz odleglosci ma ksztalt (4, 4): "
      f"{macierz_odleglosci.shape == (4, 4)}")

print(f"Czy macierz jest symetryczna: "
      f"{np.allclose(macierz_odleglosci, macierz_odleglosci.T)}")

print(f"Czy przekatna zawiera same zera: "
      f"{np.allclose(np.diag(macierz_odleglosci), 0)}")

print(f"Czy wszystkie odleglosci sa nieujemne: "
      f"{np.all(macierz_odleglosci >= 0)}")

print(f"Czy odleglosc P1-P2 jest poprawna: "
      f"{np.isclose(macierz_odleglosci[0, 1], odleglosc_euklidesowa(points[0], points[1]))}")

print(f"Czy wszystkie odleglosci sa skonczone: "
      f"{np.all(np.isfinite(macierz_odleglosci))}")
