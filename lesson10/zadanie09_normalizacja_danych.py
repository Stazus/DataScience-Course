# Lekcja 10 - Zadanie 9: Normalizacja danych

import numpy as np


# Generowanie ocen 20 studentow z 3 przedmiotow
np.random.seed(2)
scores = np.random.randint(40, 100, size=(20, 3))

# Minimum i maksimum dla kazdego przedmiotu
minimum = np.min(scores, axis=0)
maksimum = np.max(scores, axis=0)

# Normalizacja Min-Max per kolumna
zakres = maksimum - minimum

# Zabezpieczenie przed dzieleniem przez zero
bezpieczny_zakres = np.where(zakres == 0, 1, zakres)

scores_normalized = (scores - minimum) / bezpieczny_zakres


def histogram_tekstowy(dane, bins=5, zakres=None):
    liczebnosci, granice = np.histogram(
        dane, bins=bins, range=zakres
    )

    for i, liczba in enumerate(liczebnosci):
        pasek = "█" * int(liczba)

        print(
            f"{granice[i]:6.2f} - "
            f"{granice[i + 1]:6.2f} | "
            f"{pasek} ({liczba})"
        )


print("NORMALIZACJA DANYCH MIN-MAX")
print("=" * 70)

print("\nDANE ORYGINALNE")
print("=" * 70)
print(scores)
print(f"Shape: {scores.shape}")

print("\nMINIMUM I MAKSIMUM PRZED NORMALIZACJA")
print("=" * 70)
print(f"Minimum: {minimum}")
print(f"Maksimum: {maksimum}")

print("\nDANE PO NORMALIZACJI")
print("=" * 70)
print(np.round(scores_normalized, 4))

print("\nMINIMUM I MAKSIMUM PO NORMALIZACJI")
print("=" * 70)
print(f"Minimum: {np.min(scores_normalized, axis=0)}")
print(f"Maksimum: {np.max(scores_normalized, axis=0)}")

print("\nHISTOGRAMY PRZED NORMALIZACJA")
print("=" * 70)

for i in range(scores.shape[1]):
    print(f"\nPrzedmiot {i + 1}:")
    histogram_tekstowy(scores[:, i], bins=5)

print("\nHISTOGRAMY PO NORMALIZACJI")
print("=" * 70)

for i in range(scores_normalized.shape[1]):
    print(f"\nPrzedmiot {i + 1}:")
    histogram_tekstowy(
        scores_normalized[:, i],
        bins=5,
        zakres=(0, 1)
    )

print("\nWERYFIKACJA")
print("=" * 70)

print(
    f"Czy tablica ma ksztalt (20, 3): "
    f"{scores.shape == (20, 3)}"
)

print(
    f"Czy zachowano ksztalt tablicy: "
    f"{scores_normalized.shape == scores.shape}"
)

print(
    f"Czy minimum kazdego przedmiotu wynosi 0: "
    f"{np.allclose(np.min(scores_normalized, axis=0), 0)}"
)

print(
    f"Czy maksimum kazdego przedmiotu wynosi 1: "
    f"{np.allclose(np.max(scores_normalized, axis=0), 1)}"
)

print(
    f"Czy wszystkie wartosci sa w zakresie [0, 1]: "
    f"{np.all((scores_normalized >= 0) & (scores_normalized <= 1))}"
)

print(
    f"Czy nie wystepuja NaN ani nieskonczonosci: "
    f"{np.all(np.isfinite(scores_normalized))}"
)

print(
    f"Czy dane oryginalne pozostaly niezmienione: "
    f"{np.array_equal(scores, np.random.RandomState(2).randint(40, 100, size=(20, 3)))}"
)
