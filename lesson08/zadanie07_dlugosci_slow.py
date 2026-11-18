# Lekcja 08 - Zadanie 07: Dlugosci slow

# Dane wejsciowe
slowa = ["python", "data", "science", "machine", "learning", "AI"]

# List comprehension - lista dlugosci slow
dlugosci = [len(slowo) for slowo in slowa]

# Dict comprehension - slownik slowo: dlugosc
slownik = {slowo: len(slowo) for slowo in slowa}

# Wyswietlenie wynikow
print("DLUGOSCI SLOW")
print("=" * 50)

print(f"Lista slow: {slowa}")
print(f"Lista dlugosci: {dlugosci}")
print(f"Slownik: {slownik}")

# Wyswietlenie szczegolowe
print("\nDlugosci poszczegolnych slow:")

for slowo, dlugosc in slownik.items():
    print(f"{slowo:10} : {dlugosc}")

# Weryfikacja wyniku
oczekiwane = [6, 4, 7, 7, 8, 2]
print(f"\nCzy wynik jest poprawny: {dlugosci == oczekiwane}")
