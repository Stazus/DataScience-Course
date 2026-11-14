# Lekcja 07 - Zadanie 1: Parzysta czy nieparzysta

liczby = [12, 7, 23, 45, 8, 19, 34, 56, 91, 2]

for liczba in liczby:
    if liczba % 2 == 0:
        print(f"{liczba} – parzysta")
    else:
        print(f"{liczba} – nieparzysta")
