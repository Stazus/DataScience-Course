# Lekcja 07 - Zadanie 14: Korelacja Pearsona recznie

# Dane wejsciowe
wzrost = [165, 170, 175, 180, 185]
waga = [60, 65, 70, 75, 80]

# 1. Obliczenie srednich
sr_x = sum(wzrost) / len(wzrost)
sr_y = sum(waga) / len(waga)

# 2. Inicjalizacja sum
sum_xy = 0
sum_x2 = 0
sum_y2 = 0

# Obliczenie trzech sum w jednej petli
for i in range(len(wzrost)):
    sum_xy += (wzrost[i] - sr_x) * (waga[i] - sr_y)
    sum_x2 += (wzrost[i] - sr_x) ** 2
    sum_y2 += (waga[i] - sr_y) ** 2

# 3. Obliczenie wspolczynnika korelacji Pearsona
r = sum_xy / (sum_x2 * sum_y2) ** 0.5

# 4. Wyswietlenie wynikow
print("KORELACJA PEARSONA")
print("=" * 50)

print(f"Sredni wzrost: {sr_x:.2f} cm")
print(f"Srednia waga: {sr_y:.2f} kg")

print(f"\nsum_xy = {sum_xy:.2f}")
print(f"sum_x2 = {sum_x2:.2f}")
print(f"sum_y2 = {sum_y2:.2f}")

print(f"\nr = {r:.4f}")
