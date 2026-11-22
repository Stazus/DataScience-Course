# Lekcja 09 - Zadanie 2: Klasa Kalkulator


class Kalkulator:

    def dodaj(self, a, b):
        return a + b

    def odejmij(self, a, b):
        return a - b

    def pomnoz(self, a, b):
        return a * b

    def podziel(self, a, b):
        if b == 0:
            return "Blad: dzielenie przez zero!"

        return a / b


# Utworzenie obiektu klasy Kalkulator
kalkulator = Kalkulator()

# Dane wejsciowe
a = 20
b = 5

# Wykonanie obliczen
print("KALKULATOR - PROGRAMOWANIE OBIEKTOWE")
print("=" * 50)

print(f"Liczba a: {a}")
print(f"Liczba b: {b}")

print("\nWYNIKI OBLICZEN")
print("=" * 50)

print(f"Dodawanie: {a} + {b} = {kalkulator.dodaj(a, b)}")
print(f"Odejmowanie: {a} - {b} = {kalkulator.odejmij(a, b)}")
print(f"Mnozenie: {a} * {b} = {kalkulator.pomnoz(a, b)}")
print(f"Dzielenie: {a} / {b} = {kalkulator.podziel(a, b)}")

# Test dzielenia przez zero
print("\nTEST DZIELENIA PRZEZ ZERO")
print("=" * 50)

print(kalkulator.podziel(10, 0))

# Weryfikacja wynikow
print("\nWERYFIKACJA")
print("=" * 50)

print(f"Dodawanie poprawne: {kalkulator.dodaj(20, 5) == 25}")
print(f"Odejmowanie poprawne: {kalkulator.odejmij(20, 5) == 15}")
print(f"Mnozenie poprawne: {kalkulator.pomnoz(20, 5) == 100}")
print(f"Dzielenie poprawne: {kalkulator.podziel(20, 5) == 4.0}")
print(f"Obsluga dzielenia przez zero: {kalkulator.podziel(10, 0) == 'Blad: dzielenie przez zero!'}")
