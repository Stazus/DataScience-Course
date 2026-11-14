# Lekcja 07 - Zadanie 10: Liczby pierwsze do 100

liczby_pierwsze = []

# Sprawdzanie liczb od 2 do 100
for n in range(2, 101):
    czy_pierwsza = True

    # Sprawdzanie potencjalnych dzielnikow
    for dzielnik in range(2, int(n ** 0.5) + 1):
        if n % dzielnik == 0:
            czy_pierwsza = False
            break

    # Dodanie liczby pierwszej do listy
    if czy_pierwsza:
        liczby_pierwsze.append(n)

# Wyswietlenie wynikow
print("Liczby pierwsze od 2 do 100:")
print(liczby_pierwsze)
print(f"Liczba liczb pierwszych: {len(liczby_pierwsze)}")
