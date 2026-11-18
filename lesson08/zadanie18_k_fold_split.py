# Lekcja 08 - Zadanie 18: Funkcja k-fold split

# Funkcja dzielaca dane na k foldow
def k_fold_split(dane, k):
    """Dzieli dane na k rownych czesci."""

    rozmiar = len(dane) // k

    return [
        dane[i * rozmiar:(i + 1) * rozmiar]
        for i in range(k)
    ]


# Dane wejsciowe
dane = list(range(1, 101))
k = 5

# Podzial danych
foldy = k_fold_split(dane, k)

# Wyswietlenie wynikow
print("K-FOLD SPLIT")
print("=" * 70)

print(f"Liczba obserwacji: {len(dane)}")
print(f"Liczba foldow: {k}")
print(f"Rozmiar pojedynczego foldu: {len(dane) // k}")

# Wyswietlenie wszystkich foldow
print("\nPODZIAL DANYCH")
print("=" * 70)

for i, fold in enumerate(foldy, start=1):
    print(f"Fold {i}: {fold}")
    print(f"Liczba elementow: {len(fold)}")

# Weryfikacja wynikow
print("\nWERYFIKACJA")
print("=" * 70)

print(f"Czy utworzono 5 foldow: {len(foldy) == 5}")

rowne_foldy = all(len(fold) == 20 for fold in foldy)
print(f"Czy kazdy fold ma 20 elementow: {rowne_foldy}")

laczna_liczba = sum(len(fold) for fold in foldy)
print(f"Laczna liczba elementow: {laczna_liczba}")

polaczone = [x for fold in foldy for x in fold]

print(f"Czy zachowano wszystkie dane: {polaczone == dane}")
