# Lekcja 08 - Zadanie 15: Funkcje wyzszego rzedu - applicator

# Dane wejsciowe
liczby = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# Wlasna implementacja odpowiednika map()
def applicator(func, iterable):
    """Stosuje funkcje do kazdego elementu kolekcji."""
    return [func(x) for x in iterable]


# Zwykla funkcja obliczajaca pierwiastek
def sqrt(x):
    return x ** 0.5


# Test 1 - kwadraty liczb
kwadraty = applicator(lambda x: x ** 2, liczby)

# Test 2 - mnozenie przez 10
pomnozone = applicator(lambda x: x * 10, liczby)

# Test 3 - pierwiastki kwadratowe
pierwiastki = applicator(sqrt, liczby)


# Porownanie z wbudowana funkcja map()
map_kwadraty = list(map(lambda x: x ** 2, liczby))
map_pomnozone = list(map(lambda x: x * 10, liczby))
map_pierwiastki = list(map(sqrt, liczby))


# Wyswietlenie wynikow
print("FUNKCJE WYZSZEGO RZEDU - APPLICATOR")
print("=" * 60)

print(f"Dane wejsciowe: {liczby}")

print("\nTEST 1 - KWADRATY")
print(f"Applicator: {kwadraty}")
print(f"Map:        {map_kwadraty}")

print("\nTEST 2 - MNOZENIE PRZEZ 10")
print(f"Applicator: {pomnozone}")
print(f"Map:        {map_pomnozone}")

print("\nTEST 3 - PIERWIASTKI")
print(f"Applicator: {[round(x, 4) for x in pierwiastki]}")
print(f"Map:        {[round(x, 4) for x in map_pierwiastki]}")

# Weryfikacja wynikow
print("\nWERYFIKACJA")
print("=" * 60)

print(f"Kwadraty zgodne: {kwadraty == map_kwadraty}")
print(f"Mnozenie zgodne: {pomnozone == map_pomnozone}")
print(f"Pierwiastki zgodne: {pierwiastki == map_pierwiastki}")

wszystkie_zgodne = (
    kwadraty == map_kwadraty
    and pomnozone == map_pomnozone
    and pierwiastki == map_pierwiastki
)

print(f"\nCzy wszystkie wyniki sa zgodne: {wszystkie_zgodne}")
print(f"Typ zwracanych danych: {type(kwadraty).__name__}")
