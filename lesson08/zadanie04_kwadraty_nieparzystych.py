# Lekcja 08 - Zadanie 04: Kwadraty liczb nieparzystych

# Zakres liczb od 1 do 20
liczby = range(1, 21)

# Kwadraty liczb nieparzystych - list comprehension
kwadraty = [x ** 2 for x in liczby if x % 2 != 0]

# Wyswietlenie wynikow
print("KWADRATY LICZB NIEPARZYSTYCH")
print("=" * 50)

print(f"Liczby wejsciowe: {list(liczby)}")
print(f"Kwadraty liczb nieparzystych: {kwadraty}")
print(f"Liczba elementow: {len(kwadraty)}")

# Weryfikacja wyniku
oczekiwane = [1, 9, 25, 49, 81, 121, 169, 225, 289, 361]

print(f"Czy wynik jest poprawny: {kwadraty == oczekiwane}")
