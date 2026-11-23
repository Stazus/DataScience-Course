# Lekcja 10 - Zadanie 15: Konwolucja 1D

import numpy as np


def konwolucja_1d(signal, kernel):
    if len(kernel) == 0:
        raise ValueError("Kernel nie moze byc pusty.")

    if len(kernel) > len(signal):
        raise ValueError("Kernel jest dluzszy od sygnalu.")

    # Dlugosc tablicy wynikowej
    dlugosc = len(signal) - len(kernel) + 1

    result = np.zeros(dlugosc, dtype=float)

    # Petla tylko po pozycjach wyniku
    for i in range(dlugosc):
        fragment = signal[i:i + len(kernel)]

        # Mnozenie i sumowanie wektorowe
        result[i] = np.sum(fragment * kernel)

    return result


def wykres_tekstowy(dane, przesuniecie=0):
    for i, wartosc in enumerate(dane):
        slupki = "█" * int(round(wartosc))
        print(
            f"Indeks {i + przesuniecie:2d}: "
            f"{slupki:<15} {wartosc:.2f}"
        )


# Dane wejsciowe
signal = np.array(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    dtype=float
)

kernel = np.array([0.2, 0.6, 0.2])

# Kopia danych oryginalnych
signal_original = signal.copy()

# Reczna konwolucja
result = konwolucja_1d(signal, kernel)


print("KONWOLUCJA 1D - NUMPY")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Sygnal: {signal}")
print(f"Kernel: {kernel}")
print(f"Dlugosc sygnalu: {len(signal)}")
print(f"Dlugosc kernela: {len(kernel)}")
print(f"Suma wag kernela: {np.sum(kernel):.2f}")

print("\nPRZYKLAD PIERWSZEGO OBLICZENIA")
print("=" * 75)

fragment = signal[:len(kernel)]
iloczyny = fragment * kernel

print(f"Fragment sygnalu: {fragment}")
print(f"Kernel: {kernel}")
print(f"Iloczyny: {iloczyny}")
print(f"Suma iloczynow: {np.sum(iloczyny):.2f}")

print("\nWYNIK KONWOLUCJI")
print("=" * 75)
print(f"Wynik: {np.round(result, 2)}")
print(f"Dlugosc wyniku: {len(result)}")

print("\nWYKRES SYGNALU ORYGINALNEGO")
print("=" * 75)
wykres_tekstowy(signal)

print("\nWYKRES SYGNALU WYGLADZONEGO")
print("=" * 75)
wykres_tekstowy(result, przesuniecie=1)

print("\nWERYFIKACJA")
print("=" * 75)

oczekiwany_wynik = np.arange(2, 10, dtype=float)

print(f"Czy sygnal ma 10 elementow: {len(signal) == 10}")
print(f"Czy kernel ma 3 elementy: {len(kernel) == 3}")
print(f"Czy suma wag wynosi 1: {np.isclose(np.sum(kernel), 1)}")
print(f"Czy wynik ma 8 elementow: {len(result) == 8}")
print(f"Czy wynik jest poprawny: {np.allclose(result, oczekiwany_wynik)}")
print(f"Czy pierwszy wynik wynosi 2: {np.isclose(result[0], 2)}")
print(f"Czy ostatni wynik wynosi 9: {np.isclose(result[-1], 9)}")
print(f"Czy wszystkie wyniki sa skonczone: {np.all(np.isfinite(result))}")
print(f"Czy dane oryginalne pozostaly niezmienione: {np.array_equal(signal, signal_original)}")
