# Lekcja 10 - Zadanie 6: Boolean indexing

import numpy as np


# Dane wejsciowe - oceny studentow
grades = np.array([78, 45, 92, 67, 34, 88, 56, 91, 23, 85, 73, 95])

# Boolean indexing - filtrowanie ocen
wysokie_oceny = grades[grades >= 80]
niedostateczne_oceny = grades[grades < 50]

# Oceny w przedziale [60, 80)
maska_przedzialu = (grades >= 60) & (grades < 80)
oceny_w_przedziale = grades[maska_przedzialu]
liczba_ocen = np.count_nonzero(maska_przedzialu)

# Kopia tablicy - zachowanie danych oryginalnych
poprawione_oceny = grades.copy()

# Podniesienie ocen do minimum 50
poprawione_oceny[poprawione_oceny < 50] = 50


print("BOOLEAN INDEXING - ANALIZA OCEN STUDENTOW")
print("=" * 70)

print(f"Oceny oryginalne: {grades}")
print(f"Liczba wszystkich ocen: {grades.size}")

print("\nOCENY WYSOKIE (>= 80)")
print("=" * 70)
print(wysokie_oceny)
print(f"Liczba wysokich ocen: {wysokie_oceny.size}")

print("\nOCENY NIEDOSTATECZNE (< 50)")
print("=" * 70)
print(niedostateczne_oceny)
print(f"Liczba ocen niedostatecznych: {niedostateczne_oceny.size}")

print("\nOCENY W PRZEDZIALE [60, 80)")
print("=" * 70)
print(oceny_w_przedziale)
print(f"Liczba ocen w przedziale: {liczba_ocen}")

print("\nPODNIESIENIE OCEN DO MINIMUM 50")
print("=" * 70)
print(f"Przed zmiana: {grades}")
print(f"Po zmianie:   {poprawione_oceny}")

print("\nWERYFIKACJA")
print("=" * 70)

print(f"Czy wysokie oceny sa poprawne: {np.array_equal(wysokie_oceny, [92, 88, 91, 85, 95])}")
print(f"Czy niedostateczne oceny sa poprawne: {np.array_equal(niedostateczne_oceny, [45, 34, 23])}")
print(f"Czy w przedziale sa 3 oceny: {liczba_ocen == 3}")
print(f"Czy wszystkie poprawione oceny wynosza minimum 50: {np.all(poprawione_oceny >= 50)}")
print(f"Czy poprawiono 3 oceny: {np.count_nonzero(grades != poprawione_oceny) == 3}")
print(f"Czy dane oryginalne pozostaly niezmienione: {np.array_equal(grades, [78, 45, 92, 67, 34, 88, 56, 91, 23, 85, 73, 95])}")
