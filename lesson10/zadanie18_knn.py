# Lekcja 10 - Zadanie 18: k-Nearest Neighbors (distance matrix)

import numpy as np


# Generowanie 50 punktow w przestrzeni 2D
np.random.seed(10)
data = np.random.rand(50, 2) * 100

# Punkt odniesienia
query = np.array([50.0, 50.0])

# Liczba najblizszych sasiadow
k = 5

# Kopia danych oryginalnych
data_original = data.copy()

# Broadcasting - roznice wspolrzednych
roznice = data - query

# Obliczenie odleglosci Euklidesowych
odleglosci = np.sqrt(np.sum(roznice ** 2, axis=1))

# Sortowanie indeksow wedlug odleglosci
posortowane_indeksy = np.argsort(odleglosci)

# Wybor 5 najblizszych sasiadow
indeksy_knn = posortowane_indeksy[:k]

# Wspolrzedne i odleglosci najblizszych sasiadow
punkty_knn = data[indeksy_knn]
odleglosci_knn = odleglosci[indeksy_knn]


print("K-NEAREST NEIGHBORS - NUMPY")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)

print(f"Shape danych: {data.shape}")
print(f"Liczba punktow: {data.shape[0]}")
print(f"Liczba wymiarow: {data.shape[1]}")
print(f"Punkt odniesienia: {query}")
print(f"Liczba sasiadow k: {k}")

print("\nPIERWSZE 5 PUNKTOW DATASETU")
print("=" * 75)
print(np.round(data[:5], 3))

print("\nBROADCASTING")
print("=" * 75)

print(f"Shape danych: {data.shape}")
print(f"Shape query: {query.shape}")
print(f"Shape roznic: {roznice.shape}")
print(f"Shape odleglosci: {odleglosci.shape}")

print("\nODLEGLOSCI OD WSZYSTKICH 50 PUNKTOW")
print("=" * 75)
print(np.round(odleglosci, 3))

print("\n5 NAJBLIZSZYCH SASIADOW")
print("=" * 75)

print(f"{'Pozycja':>8} | {'Indeks':>8} | "
      f"{'X':>10} | {'Y':>10} | {'Odleglosc':>12}")

print("-" * 75)

# Petla tylko do wyswietlania tabeli
for i, indeks in enumerate(indeksy_knn):
    x, y = data[indeks]
    dystans = odleglosci[indeks]

    print(f"{i + 1:>8} | {indeks:>8} | "
          f"{x:>10.3f} | {y:>10.3f} | {dystans:>12.3f}")

print("\nPODSUMOWANIE")
print("=" * 75)

print(f"Indeksy najblizszych sasiadow: {indeksy_knn}")
print(f"Najmniejsza odleglosc: {np.min(odleglosci_knn):.3f}")
print(f"Najwieksza odleglosc wsrod k-NN: {np.max(odleglosci_knn):.3f}")
print(f"Srednia odleglosc k-NN: {np.mean(odleglosci_knn):.3f}")
print(f"Srednia odleglosc wszystkich punktow: {np.mean(odleglosci):.3f}")


print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy dataset ma ksztalt (50, 2): "
      f"{data.shape == (50, 2)}")

print(f"Czy query ma ksztalt (2,): "
      f"{query.shape == (2,)}")

print(f"Czy broadcasting zachowal ksztalt (50, 2): "
      f"{roznice.shape == (50, 2)}")

print(f"Czy obliczono 50 odleglosci: "
      f"{odleglosci.shape == (50,)}")

print(f"Czy znaleziono 5 sasiadow: "
      f"{indeksy_knn.size == 5}")

print(f"Czy indeksy sasiadow sa poprawne: "
      f"{np.array_equal(indeksy_knn, [44, 12, 31, 40, 13])}")

print(f"Czy odleglosci sa nieujemne: "
      f"{np.all(odleglosci >= 0)}")

print(f"Czy odleglosci k-NN sa posortowane rosnaco: "
      f"{np.all(np.diff(odleglosci_knn) >= 0)}")

print(f"Czy najblizszy sasiad jest poprawny: "
      f"{indeksy_knn[0] == np.argmin(odleglosci)}")

print(f"Czy wszystkie odleglosci sa skonczone: "
      f"{np.all(np.isfinite(odleglosci))}")

print(f"Czy dane oryginalne pozostaly niezmienione: "
      f"{np.array_equal(data, data_original)}")
