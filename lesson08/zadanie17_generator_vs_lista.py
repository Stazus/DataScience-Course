# Lekcja 08 - Zadanie 17: Generator vs Lista

# Dane wejsciowe
n = 1000

# Tworzenie listy
lista = [i ** 2 for i in range(n)]

# Tworzenie generatora
gen = (i ** 2 for i in range(n))

# Informacje o liscie
print("GENERATOR VS LISTA")
print("=" * 60)

print("\nLISTA")
print(f"Typ: {type(lista)}")
print(f"Pierwsze 5 elementow: {lista[:5]}")
print(f"Liczba elementow: {len(lista)}")

# Pobranie pierwszych 5 elementow generatora
pierwsze_gen = []

for wartosc in gen:
    pierwsze_gen.append(wartosc)

    if len(pierwsze_gen) == 5:
        break

# Informacje o generatorze
print("\nGENERATOR")
print(f"Typ: {type(gen)}")
print(f"Pierwsze 5 elementow: {pierwsze_gen}")

# Proba sprawdzenia dlugosci generatora
try:
    print(f"Liczba elementow: {len(gen)}")
except TypeError:
    print("Brak obslugi len() dla generatora")

# Weryfikacja
print("\nWERYFIKACJA")
print("=" * 60)

print(f"Czy pierwsze 5 elementow jest zgodnych: {lista[:5] == pierwsze_gen}")

# Demonstracja kontynuacji generatora
print(f"Kolejny element generatora: {next(gen)}")

# Podsumowanie
print("\nPODSUMOWANIE")
print("=" * 60)
print("Lista tworzy wszystkie elementy od razu.")
print("Generator tworzy elementy tylko wtedy, gdy sa potrzebne.")
print("Lista obsluguje len() i indeksowanie.")
print("Generator nie obsluguje len() ani indeksowania.")
print("Generator pamieta miejsce zakonczenia iteracji.")
