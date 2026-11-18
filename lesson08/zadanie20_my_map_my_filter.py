# Lekcja 08 - Zadanie 20: Wlasne implementacje my_map i my_filter

# Dane wejsciowe
liczby = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# Wlasna implementacja map()
def my_map(func, iterable):
    """Stosuje funkcje do kazdego elementu kolekcji."""

    wynik = []

    for element in iterable:
        wynik.append(func(element))

    return wynik


# Wlasna implementacja filter()
def my_filter(predicate, iterable):
    """Zwraca elementy spelniajace warunek."""

    wynik = []

    for element in iterable:
        if predicate(element):
            wynik.append(element)

    return wynik


# Test 1 - podwojenie liczb
podwojone = my_map(lambda x: x * 2, liczby)

# Test 2 - filtrowanie liczb parzystych
parzyste = my_filter(lambda x: x % 2 == 0, podwojone)

# Porownanie z wbudowanymi funkcjami
map_wbudowany = list(map(lambda x: x * 2, liczby))

filter_wbudowany = list(
    filter(lambda x: x % 2 == 0, map_wbudowany)
)


# Wyswietlenie wynikow
print("WLASNE IMPLEMENTACJE MY_MAP I MY_FILTER")
print("=" * 65)

print(f"Dane wejsciowe: {liczby}")

print("\nTEST 1 - PODWOJENIE LICZB")
print(f"my_map: {podwojone}")
print(f"map:    {map_wbudowany}")

print("\nTEST 2 - FILTROWANIE LICZB PARZYSTYCH")
print(f"my_filter: {parzyste}")
print(f"filter:    {filter_wbudowany}")


# Dodatkowy test filtrowania danych oryginalnych
print("\nTEST 3 - FILTROWANIE DANYCH ORYGINALNYCH")

parzyste_oryginalne = my_filter(
    lambda x: x % 2 == 0, liczby
)

parzyste_wbudowane = list(
    filter(lambda x: x % 2 == 0, liczby)
)

print(f"my_filter: {parzyste_oryginalne}")
print(f"filter:    {parzyste_wbudowane}")


# Weryfikacja wynikow
print("\nWERYFIKACJA")
print("=" * 65)

zgodnosc_map = podwojone == map_wbudowany
zgodnosc_filter = parzyste == filter_wbudowany
zgodnosc_testu3 = parzyste_oryginalne == parzyste_wbudowane

print(f"Czy my_map jest zgodne z map: {zgodnosc_map}")
print(f"Czy my_filter jest zgodne z filter: {zgodnosc_filter}")
print(f"Czy dodatkowy test jest poprawny: {zgodnosc_testu3}")

print(f"\nCzy wszystkie testy sa poprawne: "
      f"{zgodnosc_map and zgodnosc_filter and zgodnosc_testu3}")

print(f"Typ wyniku my_map: {type(podwojone).__name__}")
print(f"Typ wyniku my_filter: {type(parzyste).__name__}")
