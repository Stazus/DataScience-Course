# Lekcja 10 - Zadanie 13: Standaryzacja i wykrywanie outlierow

import numpy as np


# Generowanie danych
np.random.seed(42)

data = np.concatenate([
    np.random.randn(100) * 10 + 50,
    np.array([150, -50, 200, -100, 180])
])

np.random.shuffle(data)

# Kopia danych oryginalnych
data_original = data.copy()


def standaryzacja(dane):
    srednia = np.mean(dane)
    odchylenie = np.std(dane)

    if odchylenie == 0:
        return np.zeros_like(dane, dtype=float)

    return (dane - srednia) / odchylenie


def statystyki(dane):
    print(f"Liczba elementow: {dane.size}")
    print(f"Srednia: {np.mean(dane):.4f}")
    print(f"Odchylenie standardowe: {np.std(dane):.4f}")
    print(f"Minimum: {np.min(dane):.4f}")
    print(f"Maksimum: {np.max(dane):.4f}")


def histogram_tekstowy(dane, bins=10, zakres=None):
    liczebnosci, granice = np.histogram(
        dane, bins=bins, range=zakres
    )

    for i, liczba in enumerate(liczebnosci):
        slupek = "█" * int(liczba)

        print(
            f"{granice[i]:8.2f} - "
            f"{granice[i + 1]:8.2f} | "
            f"{slupek} ({liczba})"
        )


# Standaryzacja danych oryginalnych
z_scores = standaryzacja(data)

# Wykrywanie wartosci odstajacych
maska_outlierow = np.abs(z_scores) > 3

outliery = data[maska_outlierow]
z_scores_outlierow = z_scores[maska_outlierow]

# Usuwanie wartosci odstajacych
data_clean = data[~maska_outlierow]

# Ponowna standaryzacja oczyszczonych danych
z_scores_clean = standaryzacja(data_clean)

# Wspolny zakres histogramow
zakres_histogramu = (np.min(data), np.max(data))


print("STANDARYZACJA I WYKRYWANIE OUTLIEROW")
print("=" * 75)

print("\nSTATYSTYKI PRZED OCZYSZCZENIEM")
print("=" * 75)
statystyki(data)

print("\nSTATYSTYKI PO PIERWSZEJ STANDARYZACJI")
print("=" * 75)
statystyki(z_scores)

print("\nWYKRYTE OUTLIERY")
print("=" * 75)

for wartosc, z in zip(outliery, z_scores_outlierow):
    print(f"Wartosc: {wartosc:8.2f} | Z-score: {z:8.4f}")

print(f"\nLiczba wykrytych outlierow: {outliery.size}")

print("\nSTATYSTYKI PO USUNIECIU OUTLIEROW")
print("=" * 75)
statystyki(data_clean)

print("\nSTATYSTYKI PO PONOWNEJ STANDARYZACJI")
print("=" * 75)
statystyki(z_scores_clean)

print("\nHISTOGRAM PRZED OCZYSZCZENIEM")
print("=" * 75)
histogram_tekstowy(data, zakres=zakres_histogramu)

print("\nHISTOGRAM PO OCZYSZCZENIU")
print("=" * 75)
histogram_tekstowy(data_clean, zakres=zakres_histogramu)

print("\nPODSUMOWANIE")
print("=" * 75)

print(f"Liczba danych przed: {data.size}")
print(f"Liczba danych po: {data_clean.size}")
print(f"Liczba usunietych wartosci: {outliery.size}")
print(f"Procent usunietych danych: {outliery.size / data.size * 100:.2f}%")

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy poczatkowo bylo 105 elementow: {data.size == 105}")

print(
    f"Czy wykryto 5 outlierow: "
    f"{outliery.size == 5}"
)

print(
    f"Czy wykryto poprawne wartosci odstajace: "
    f"{np.array_equal(np.sort(outliery), [-100, -50, 150, 180, 200])}"
)

print(f"Czy pozostalo 100 elementow: {data_clean.size == 100}")

print(
    f"Czy srednia po pierwszej standaryzacji wynosi 0: "
    f"{np.isclose(np.mean(z_scores), 0)}"
)

print(
    f"Czy odchylenie po pierwszej standaryzacji wynosi 1: "
    f"{np.isclose(np.std(z_scores), 1)}"
)

print(
    f"Czy srednia po ponownej standaryzacji wynosi 0: "
    f"{np.isclose(np.mean(z_scores_clean), 0)}"
)

print(
    f"Czy odchylenie po ponownej standaryzacji wynosi 1: "
    f"{np.isclose(np.std(z_scores_clean), 1)}"
)

print(
    f"Czy wszystkie wykryte outliery maja |z| > 3: "
    f"{np.all(np.abs(z_scores_outlierow) > 3)}"
)

print(
    f"Czy zachowano dane oryginalne: "
    f"{np.array_equal(data, data_original)}"
)
