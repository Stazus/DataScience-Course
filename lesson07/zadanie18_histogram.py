# Lekcja 07 - Zadanie 18: Histogram (binning)

# Dane wejsciowe
dane = [
    12, 15, 18, 22, 25, 28, 31, 35,
    38, 42, 45, 48, 52, 55, 58
]

# Granice przedzialow i liczniki
granice = [10, 20, 30, 40, 50, 60]
biny = [0, 0, 0, 0, 0]

# Przypisywanie wartosci do odpowiednich przedzialow
for x in dane:
    for i in range(5):
        if granice[i] <= x < granice[i + 1]:
            biny[i] += 1
            break

# Wyswietlenie histogramu tekstowego
print("HISTOGRAM - BINNING")
print("=" * 50)

for i in range(5):
    gwiazdki = "*" * biny[i]
    print(f"[{granice[i]}, {granice[i + 1]}): {gwiazdki}")

# Podsumowanie
print(f"\nLiczba danych: {len(dane)}")
print(f"Liczniki binow: {biny}")
print(f"Suma licznikow: {sum(biny)}")
