# Lekcja 07 - Zadanie 19: Macierz przejsc (transition matrix)

# Sekwencja stanow
stany = ['A', 'B', 'A', 'A', 'C', 'B', 'C', 'A', 'B', 'B']

# 1. Wyznaczenie unikalnych stanow
unikalne = sorted(set(stany))

# 2. Utworzenie slownika slownikow
przejscia = {}

for s1 in unikalne:
    for s2 in unikalne:
        przejscia.setdefault(s1, {}).setdefault(s2, 0)

# 3. Zliczanie przejsc pomiedzy stanami
for i in range(len(stany) - 1):
    przejscia[stany[i]][stany[i + 1]] += 1

# 4. Wyswietlenie macierzy przejsc
print("MACIERZ PRZEJSC")
print("=" * 50)
print(f"Sekwencja stanow: {stany}")
print(f"Unikalne stany: {unikalne}")

print("\nMacierz przejsc:")

# Naglowek tabeli
print("    ", end="")

for s2 in unikalne:
    print(f"{s2:>4}", end="")

print()

# Wiersze macierzy
for s1 in unikalne:
    print(f"{s1:>4}", end="")

    for s2 in unikalne:
        print(f"{przejscia[s1][s2]:>4}", end="")

    print()

# Podsumowanie
print(f"\nLiczba stanow: {len(stany)}")
print(f"Liczba przejsc: {len(stany) - 1}")
