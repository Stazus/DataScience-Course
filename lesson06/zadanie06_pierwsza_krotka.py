# Lekcja 06 - Zadanie 6: Pierwsza krotka

# Utworzenie krotki z wymiarami
wymiary = (1920, 1080)

# Rozpakowanie krotki
szerokosc, wysokosc = wymiary

# Wyświetlenie rozdzielczości
print(f"Rozdzielczość: {szerokosc}x{wysokosc}")

# Utworzenie krotki jednoelementowej
samotny = (42,)

# Wyświetlenie krotki i jej typu
print(f"Krotka jednoelementowa: {samotny}")
print(f"Typ: {type(samotny)}")

# Próba modyfikacji krotki
# samotny[0] = 100
# TypeError: 'tuple' object does not support item assignment

# Utworzenie nowej krotki przez połączenie
nowa_krotka = samotny + (100, 200)

# Wyświetlenie wyników
print(f"Nowa krotka: {nowa_krotka}")
print(f"Oryginalna krotka: {samotny}")
