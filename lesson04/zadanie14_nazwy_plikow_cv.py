# Lekcja 04 - Zadanie 14: Generowanie nazw plików dla cross-validation

dataset = "iris"
liczba_foldow = 5
typy = ["train", "test"]

liczba_plikow = 0

# Generowanie nazw plików dla kolejnych foldów
for fold in range(1, liczba_foldow + 1):
    for typ in typy:
        nazwa_pliku = f"{dataset}_fold_{fold:02d}_{typ}.csv"
        print(nazwa_pliku)
        liczba_plikow += 1

print(f"\nŁączna liczba plików: {liczba_plikow}")
