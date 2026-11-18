# Lekcja 08 - Zadanie 12: Zagniezdzone comprehensions - macierz

# Rozmiar macierzy
n = 10

# Tworzenie macierzy - zagniezdzone list comprehension
macierz = [
    [i * j for j in range(1, n + 1)]
    for i in range(1, n + 1)
]

# Wyswietlenie macierzy
print("MACIERZ 10 x 10")
print("=" * 50)

for wiersz in macierz:
    print(" ".join(f"{wartosc:4}" for wartosc in wiersz))

# Weryfikacja wynikow
print("\nWERYFIKACJA")
print("=" * 50)

print(f"Liczba wierszy: {len(macierz)}")
print(f"Liczba kolumn: {len(macierz[0])}")
print(f"Liczba elementow: {sum(len(wiersz) for wiersz in macierz)}")
print(f"Pierwszy element: {macierz[0][0]}")
print(f"Ostatni element: {macierz[-1][-1]}")

poprawny_rozmiar = (
    len(macierz) == 10
    and all(len(wiersz) == 10 for wiersz in macierz)
)

print(f"Czy macierz ma rozmiar 10 x 10: {poprawny_rozmiar}")
