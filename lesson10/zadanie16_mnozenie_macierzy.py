# Lekcja 10 - Zadanie 16: Matrix multiplication (dot product)

import numpy as np
from time import perf_counter


def mnozenie_macierzy(A, B):
    if A.shape[1] != B.shape[0]:
        raise ValueError("Niezgodne wymiary macierzy.")

    wiersze = A.shape[0]
    kolumny = B.shape[1]
    wspolny_wymiar = A.shape[1]

    C = np.zeros((wiersze, kolumny), dtype=float)

    # Trzy zagniezdzone petle
    for i in range(wiersze):
        for j in range(kolumny):
            for k in range(wspolny_wymiar):
                C[i, j] += A[i, k] * B[k, j]

    return C


# Generowanie danych
np.random.seed(5)

A = np.random.rand(100, 50)
B = np.random.rand(50, 20)

# Kopie danych oryginalnych
A_original = A.copy()
B_original = B.copy()

# Mnozenie macierzy przez NumPy
start = perf_counter()

C_np = A @ B

czas_numpy = perf_counter() - start

# Reczne mnozenie macierzy
start = perf_counter()

C_loop = mnozenie_macierzy(A, B)

czas_petle = perf_counter() - start

# Porownanie wynikow
zgodnosc = np.allclose(C_np, C_loop)
maksymalna_roznica = np.max(np.abs(C_np - C_loop))

# Porownanie wydajnosci
przyspieszenie = (
    czas_petle / czas_numpy
    if czas_numpy > 0 else np.inf
)


print("MNOZENIE MACIERZY - NUMPY VS PYTHON")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape A: {A.shape}")
print(f"Shape B: {B.shape}")
print(f"Liczba elementow A: {A.size}")
print(f"Liczba elementow B: {B.size}")

print("\nMNOZENIE MACIERZY - NUMPY")
print("=" * 75)
print(f"Shape C_np: {C_np.shape}")
print("Fragment macierzy wynikowej (5x5):")
print(np.round(C_np[:5, :5], 4))

print("\nMNOZENIE MACIERZY - TRZY PETLE")
print("=" * 75)
print(f"Shape C_loop: {C_loop.shape}")
print("Fragment macierzy wynikowej (5x5):")
print(np.round(C_loop[:5, :5], 4))

print("\nPOROWNANIE WYNIKOW")
print("=" * 75)
print(f"Zgodnosc np.allclose(): {zgodnosc}")
print(f"Maksymalna roznica: {maksymalna_roznica:.12e}")

print("\nPOROWNANIE WYDAJNOSCI")
print("=" * 75)
print(f"Czas NumPy: {czas_numpy:.8f} s")
print(f"Czas petli: {czas_petle:.8f} s")
print(f"Przyspieszenie NumPy: {przyspieszenie:.2f}x")

liczba_mnozen = A.shape[0] * A.shape[1] * B.shape[1]

print(f"Liczba operacji mnozenia: {liczba_mnozen:,}")

print("\nDLACZEGO NUMPY JEST SZYBSZE?")
print("=" * 75)
print("1. Wykorzystuje operacje wektorowe.")
print("2. Wykonuje obliczenia w skompilowanym kodzie.")
print("3. Moze korzystac z bibliotek BLAS.")
print("4. Ogranicza narzut interpretera Pythona.")
print("5. Efektywnie wykorzystuje pamiec i procesor.")
print("6. Moze wykorzystywac instrukcje SIMD i wielowatkowosc.")

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy A ma ksztalt (100, 50): {A.shape == (100, 50)}")
print(f"Czy B ma ksztalt (50, 20): {B.shape == (50, 20)}")
print(f"Czy C_np ma ksztalt (100, 20): {C_np.shape == (100, 20)}")
print(f"Czy C_loop ma ksztalt (100, 20): {C_loop.shape == (100, 20)}")
print(f"Czy wynik ma 2000 elementow: {C_np.size == 2000}")
print(f"Czy wyniki sa zgodne: {np.allclose(C_np, C_loop)}")
print(f"Czy pierwszy element jest poprawny: {np.isclose(C_np[0, 0], np.sum(A[0, :] * B[:, 0]))}")
print(f"Czy wszystkie wyniki sa skonczone: {np.all(np.isfinite(C_np))}")
print(f"Czy macierz A pozostala niezmieniona: {np.array_equal(A, A_original)}")
print(f"Czy macierz B pozostala niezmieniona: {np.array_equal(B, B_original)}")
