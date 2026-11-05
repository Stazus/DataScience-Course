# Lekcja 04 - Zadanie 3: Podział zbioru danych

liczba_probek = 1000

trening = liczba_probek * 70 // 100
walidacja = liczba_probek * 15 // 100
test = liczba_probek - trening - walidacja

suma = trening + walidacja + test

print(f"Zbiór treningowy: {trening}")
print(f"Zbiór walidacyjny: {walidacja}")
print(f"Zbiór testowy: {test}")
print(f"Suma próbek: {suma}")
