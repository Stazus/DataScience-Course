# Lekcja 04 - Zadanie 13: Detekcja anomalii metodą 3-sigma

pomiary = [120, 125, 118, 190, 122]

# Obliczenie średniej
liczba_pomiarow = len(pomiary)
srednia = sum(pomiary) / liczba_pomiarow

# Obliczenie wariancji i odchylenia standardowego
suma_kwadratow = 0

for pomiar in pomiary:
    suma_kwadratow += (pomiar - srednia) ** 2

wariancja = suma_kwadratow / liczba_pomiarow
odchylenie_std = wariancja ** 0.5

# Granice reguły 3-sigma
dolna_granica = srednia - 3 * odchylenie_std
gorna_granica = srednia + 3 * odchylenie_std

print(f"Średnia: {srednia:.2f}")
print(f"Odchylenie standardowe: {odchylenie_std:.2f}")
print(f"Przedział 3-sigma: [{dolna_granica:.2f}, {gorna_granica:.2f}]")

print("\nRaport pomiarów:")

for pomiar in pomiary:
    if abs(pomiar - srednia) > 3 * odchylenie_std:
        status = "ANOMALIA!"
    else:
        status = "OK"

    print(f"Wartość: {pomiar} - {status}")

# Uwaga:
# W przykładzie LearnIT wartość 190 oznaczono jako anomalię.
# Jednak przy zastosowaniu reguły 3-sigma do podanych
# pięciu pomiarów żadna wartość nie przekracza granic.
# Program zachowuje matematycznie poprawną regułę 3-sigma.
