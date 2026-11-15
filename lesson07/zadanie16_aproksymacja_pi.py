# Lekcja 07 - Zadanie 16: Aproksymacja pi metoda Leibniza

# Liczba iteracji
n = 1_000_000
suma = 0

# Obliczanie szeregu Leibniza
for i in range(n):
    licznik = (-1) ** i
    mianownik = 2 * i + 1

    suma += licznik / mianownik

# Obliczenie przyblizonej wartosci pi
pi_aproksymacja = 4 * suma

# Wartosc referencyjna pi
pi_prawdziwe = 3.141593

# Obliczenie bledu bezwzglednego
blad = abs(pi_aproksymacja - pi_prawdziwe)

# Wyswietlenie wynikow
print("APROKSYMACJA PI - METODA LEIBNIZA")
print("=" * 50)
print(f"Liczba iteracji: {n}")
print(f"Aproksymacja pi: {pi_aproksymacja:.6f}")
print(f"Wartosc referencyjna pi: {pi_prawdziwe:.6f}")
print(f"Blad bezwzgledny: {blad:.10f}")
