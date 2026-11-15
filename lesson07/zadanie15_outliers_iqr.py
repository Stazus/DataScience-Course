# Lekcja 07 - Zadanie 15: Outliers metoda IQR

# Dane wejsciowe
wyniki = [
    78, 82, 85, 88, 90, 92, 95,
    97, 99, 45, 101, 103, 105, 180
]

# 1. Sortowanie danych
posort = sorted(wyniki)

# 2. Wyznaczenie kwartylow
Q1 = posort[len(posort) // 4]
Q3 = posort[3 * len(posort) // 4]

# 3. Obliczenie rozstepu miedzykwartylowego
IQR = Q3 - Q1

# Wyznaczenie granic
dolna = Q1 - 1.5 * IQR
gorna = Q3 + 1.5 * IQR

# 4. Wykrywanie wartosci odstajacych
outliers = [
    x for x in wyniki
    if x < dolna or x > gorna
]

# 5. Wyswietlenie wynikow
print("DETEKCJA OUTLIERS - METODA IQR")
print("=" * 50)

print(f"Dane oryginalne: {wyniki}")
print(f"Dane posortowane: {posort}")

print(f"\nQ1 = {Q1}")
print(f"Q3 = {Q3}")
print(f"IQR = {IQR}")

print(f"\nDolna granica: {dolna}")
print(f"Gorna granica: {gorna}")

print(f"\nOutliers: {outliers}")
print(f"Liczba outliers: {len(outliers)}")
