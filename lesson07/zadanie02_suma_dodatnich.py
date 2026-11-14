# Lekcja 07 - Zadanie 2: Suma liczb dodatnich

liczby = [-5, 3, -2, 8, 12, -1, 6, 0, 15, -3]

suma_dodatnich = 0
licznik_dodatnich = 0

# Sumowanie i zliczanie liczb dodatnich
for temp in liczby:
    if temp > 0:
        suma_dodatnich += temp
        licznik_dodatnich += 1

# Wyswietlenie wynikow
print(f"Suma liczb dodatnich: {suma_dodatnich}")
print(f"Liczba dodatnich wartosci: {licznik_dodatnich}")
