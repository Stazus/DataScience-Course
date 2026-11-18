# Lekcja 08 - Zadanie 16: Rekurencja - silnia i Fibonacci


# Funkcja rekurencyjna obliczajaca silnie
def silnia(n):
    """Oblicza silnie liczby n."""

    if n == 0:
        return 1

    return n * silnia(n - 1)


# Funkcja rekurencyjna obliczajaca liczbe Fibonacciego
def fibonacci(n):
    """Oblicza n-ta liczbe Fibonacciego."""

    if n == 0:
        return 0

    if n == 1:
        return 1

    return fibonacci(n - 1) + fibonacci(n - 2)


# Dane wejsciowe
n_silnia = 10
n_fibonacci = 15

# Obliczenie silni
wynik_silnia = silnia(n_silnia)

# Generowanie ciagu Fibonacciego - list comprehension
ciag_fibonacciego = [
    fibonacci(i) for i in range(n_fibonacci)
]

# Wyswietlenie wynikow
print("REKURENCJA - SILNIA I FIBONACCI")
print("=" * 60)

print("\nSILNIA")
print(f"silnia({n_silnia}) = {wynik_silnia}")

print("\nCIAG FIBONACCIEGO")
print(f"Pierwsze {n_fibonacci} liczb:")
print(ciag_fibonacciego)

# Weryfikacja wynikow
oczekiwana_silnia = 3628800

oczekiwany_fibonacci = [
    0, 1, 1, 2, 3, 5, 8, 13,
    21, 34, 55, 89, 144, 233, 377
]

print("\nWERYFIKACJA")
print("=" * 60)

print(f"Czy silnia jest poprawna: {wynik_silnia == oczekiwana_silnia}")
print(f"Czy Fibonacci jest poprawny: {ciag_fibonacciego == oczekiwany_fibonacci}")
print(f"Liczba elementow ciagu: {len(ciag_fibonacciego)}")
