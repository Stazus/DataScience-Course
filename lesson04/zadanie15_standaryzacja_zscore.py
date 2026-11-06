# Lekcja 04 - Zadanie 15: Standaryzacja Z-score

wagi = [65.5, 78.2, 54.8, 92.1, 70.0]

# Obliczenie średniej
liczba_pomiarow = len(wagi)
srednia = sum(wagi) / liczba_pomiarow

# Obliczenie odchylenia standardowego
suma_kwadratow = 0

for waga in wagi:
    suma_kwadratow += (waga - srednia) ** 2

wariancja = suma_kwadratow / liczba_pomiarow
odchylenie_std = wariancja ** 0.5

# Standaryzacja wartości
z_scores = []

for waga in wagi:
    z = (waga - srednia) / odchylenie_std
    z_scores.append(z)

# Sprawdzenie średniej i odchylenia Z-score
srednia_z = sum(z_scores) / len(z_scores)

wariancja_z = sum((z - srednia_z) ** 2 for z in z_scores) / len(z_scores)
odchylenie_z = wariancja_z ** 0.5

print(f"Średnia wag: {srednia:.2f} kg")
print(f"Odchylenie standardowe wag: {odchylenie_std:.4f}")

print("\nRaport standaryzacji:")
print(f"{'Waga (kg)':<12} {'Z-score':<12} {'Interpretacja'}")
print("-" * 45)

for waga, z in zip(wagi, z_scores):
    if z > 2:
        interpretacja = "Bardzo wysoka"
    elif z < -2:
        interpretacja = "Bardzo niska"
    elif abs(z) < 1:
        interpretacja = "Typowa"
    else:
        interpretacja = "Umiarkowanie odchylona"

    print(f"{waga:<12.1f} {z:<12.4f} {interpretacja}")

print("\nKontrola standaryzacji:")
print(f"Średnia Z-score: {srednia_z:.6f}")
print(f"Odchylenie standardowe Z-score: {odchylenie_z:.6f}")

print(f"Średnia ≈ 0: {abs(srednia_z) < 1e-10}")
print(f"Odchylenie ≈ 1: {abs(odchylenie_z - 1) < 1e-10}")
