# Lekcja 07 - Zadanie 17: Algorytm Euklidesa (NWD)

# Dane wejsciowe
a = 252
b = 105

iteracje = 0

print("ALGORYTM EUKLIDESA")
print("=" * 50)
print(f"Liczby wejsciowe: {a}, {b}")

# Obliczanie najwiekszego wspolnego dzielnika
while b != 0:
    a, b = b, a % b
    iteracje += 1

# Wyswietlenie wynikow
print(f"NWD = {a}")
print(f"Liczba iteracji: {iteracje}")
