# Lekcja 08 - Zadanie 05: Lambda do sortowania

# Dane wejsciowe
produkty = [
    ("laptop", 2999, 4.5),
    ("mysz", 89, 4.2),
    ("klawiatura", 249, 4.8),
    ("monitor", 899, 4.3)
]

# Sortowanie wedlug ceny rosnaco
wedlug_ceny = sorted(produkty, key=lambda x: x[1])

# Sortowanie wedlug oceny malejaco
wedlug_oceny = sorted(
    produkty, key=lambda x: x[2], reverse=True
)

# Wyswietlenie wynikow
print("SORTOWANIE PRODUKTOW")
print("=" * 50)

print("\nProdukty wedlug ceny rosnaco:")
for nazwa, cena, ocena in wedlug_ceny:
    print(f"{nazwa:12} | Cena: {cena:4} zl | Ocena: {ocena}")

print("\nProdukty wedlug oceny malejaco:")
for nazwa, cena, ocena in wedlug_oceny:
    print(f"{nazwa:12} | Cena: {cena:4} zl | Ocena: {ocena}")
