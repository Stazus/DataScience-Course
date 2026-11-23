# Lekcja 10 - Zadanie 20: Symulacja Batch Normalization

import numpy as np


# Generowanie mini-batcha: 32 probki, 10 cech
np.random.seed(8)
batch = np.random.randn(32, 10) * 5 + 20

# Kopia danych oryginalnych
batch_original = batch.copy()

# Parametry scale i shift
gamma = 2.0
beta = 1.0

# Srednia i odchylenie standardowe per cecha
mean = np.mean(batch, axis=0)
std = np.std(batch, axis=0)

# Zabezpieczenie przed dzieleniem przez zero
safe_std = np.where(std == 0, 1, std)

# Batch Normalization - broadcasting
batch_norm = (batch - mean) / safe_std

# Transformacja scale i shift
output = gamma * batch_norm + beta


def wyswietl_statystyki(dane):
    print(f"Shape: {dane.shape}")
    print(f"Srednie: {np.mean(dane, axis=0)}")
    print(f"Odchylenia: {np.std(dane, axis=0)}")
    print(f"Minima: {np.min(dane, axis=0)}")
    print(f"Maksima: {np.max(dane, axis=0)}")


def histogram_tekstowy(dane, bins=8):
    liczebnosci, granice = np.histogram(dane, bins=bins)

    for i, liczba in enumerate(liczebnosci):
        slupek = "█" * int(liczba)

        print(
            f"{granice[i]:8.2f} - "
            f"{granice[i + 1]:8.2f} | "
            f"{slupek} ({liczba})"
        )


# Ustawienia wyswietlania
np.set_printoptions(precision=4, suppress=True)


print("SYMULACJA BATCH NORMALIZATION - NUMPY")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Liczba probek: {batch.shape[0]}")
print(f"Liczba cech: {batch.shape[1]}")
print(f"Liczba elementow: {batch.size}")
print(f"Gamma: {gamma}")
print(f"Beta: {beta}")

print("\nPIERWSZE 5 PROBEK PRZED NORMALIZACJA")
print("=" * 75)
print(batch[:5])

print("\nSTATYSTYKI PRZED NORMALIZACJA")
print("=" * 75)
wyswietl_statystyki(batch)

print("\nBROADCASTING")
print("=" * 75)
print(f"Shape batch: {batch.shape}")
print(f"Shape mean: {mean.shape}")
print(f"Shape std: {std.shape}")
print(f"Shape batch_norm: {batch_norm.shape}")

print("\nBATCH PO NORMALIZACJI")
print("=" * 75)
print(batch_norm)

print("\nSTATYSTYKI PO NORMALIZACJI")
print("=" * 75)
wyswietl_statystyki(batch_norm)

print("\nBATCH PO TRANSFORMACJI SCALE/SHIFT")
print("=" * 75)
print(output)

print("\nSTATYSTYKI PO TRANSFORMACJI SCALE/SHIFT")
print("=" * 75)
wyswietl_statystyki(output)

print("\nPOROWNANIE STATYSTYK PER CECHA")
print("=" * 75)

print(
    f"{'Cecha':>5} | "
    f"{'Mean przed':>11} | "
    f"{'Std przed':>10} | "
    f"{'Mean norm':>10} | "
    f"{'Std norm':>9} | "
    f"{'Mean out':>9} | "
    f"{'Std out':>8}"
)

print("-" * 85)

for i in range(batch.shape[1]):
    print(
        f"{i:5d} | "
        f"{mean[i]:11.4f} | "
        f"{std[i]:10.4f} | "
        f"{np.mean(batch_norm[:, i]):10.4f} | "
        f"{np.std(batch_norm[:, i]):9.4f} | "
        f"{np.mean(output[:, i]):9.4f} | "
        f"{np.std(output[:, i]):8.4f}"
    )

print("\nHISTOGRAM CECHY 0 - PRZED NORMALIZACJA")
print("=" * 75)
histogram_tekstowy(batch[:, 0])

print("\nHISTOGRAM CECHY 0 - PO NORMALIZACJI")
print("=" * 75)
histogram_tekstowy(batch_norm[:, 0])

print("\nHISTOGRAM CECHY 0 - PO SCALE/SHIFT")
print("=" * 75)
histogram_tekstowy(output[:, 0])

print("\nPODSUMOWANIE")
print("=" * 75)
print("Batch Normalization: zakonczona")
print("Normalizacja: mean = 0, std = 1")
print("Scale/shift: mean = 1, std = 2")
print(f"Shape danych wynikowych: {output.shape}")

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy batch ma ksztalt (32, 10): {batch.shape == (32, 10)}")
print(f"Czy batch ma 320 elementow: {batch.size == 320}")
print(f"Czy mean ma ksztalt (10,): {mean.shape == (10,)}")
print(f"Czy std ma ksztalt (10,): {std.shape == (10,)}")
print(f"Czy std jest dodatnie: {np.all(std > 0)}")
print(f"Czy normalizacja zachowala ksztalt: {batch_norm.shape == batch.shape}")
print(f"Czy output zachowal ksztalt: {output.shape == batch.shape}")
print(f"Czy mean po normalizacji wynosi 0: {np.allclose(np.mean(batch_norm, axis=0), 0)}")
print(f"Czy std po normalizacji wynosi 1: {np.allclose(np.std(batch_norm, axis=0), 1)}")
print(f"Czy mean po scale/shift wynosi 1: {np.allclose(np.mean(output, axis=0), beta)}")
print(f"Czy std po scale/shift wynosi 2: {np.allclose(np.std(output, axis=0), abs(gamma))}")
print(f"Czy transformacja jest poprawna: {np.allclose(output, gamma * batch_norm + beta)}")
print(f"Czy batch_norm zawiera skonczone wartosci: {np.all(np.isfinite(batch_norm))}")
print(f"Czy output zawiera skonczone wartosci: {np.all(np.isfinite(output))}")
print(f"Czy dane oryginalne pozostaly niezmienione: {np.array_equal(batch, batch_original)}")
