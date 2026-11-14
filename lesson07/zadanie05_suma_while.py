# Lekcja 07 - Zadanie 5: Suma przez while

n = 50
liczba = 1
suma = 0

# Sumowanie liczb za pomoca petli while
while liczba <= n:
    suma += liczba
    liczba += 1

# Sprawdzenie wyniku wzorem matematycznym
suma_wzor = n * (n + 1) / 2

# Wyswietlenie wynikow
print(f"Suma liczb od 1 do {n}: {suma}")
print(f"Wynik ze wzoru: {suma_wzor:.0f}")
print(f"Czy wyniki sa zgodne: {suma == suma_wzor}")
