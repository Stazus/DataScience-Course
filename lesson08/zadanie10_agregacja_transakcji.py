# Lekcja 08 - Zadanie 10: Dictionary comprehension - agregacja

# Dane wejsciowe
transakcje = [
    {"produkt": "laptop", "wartosc": 2999},
    {"produkt": "mysz", "wartosc": 89},
    {"produkt": "laptop", "wartosc": 2999},
    {"produkt": "klawiatura", "wartosc": 249},
    {"produkt": "mysz", "wartosc": 89},
    {"produkt": "mysz", "wartosc": 89}
]

# Grupowanie i sumowanie wartosci produktow
agregacja = {}

for transakcja in transakcje:
    produkt = transakcja["produkt"]
    wartosc = transakcja["wartosc"]

    agregacja[produkt] = agregacja.get(produkt, 0) + wartosc

# Dictionary comprehension - utworzenie slownika wynikowego
wynik = {
    produkt: suma
    for produkt, suma in agregacja.items()
}

# Wyswietlenie wynikow
print("AGREGACJA TRANSAKCJI")
print("=" * 50)

print(f"Liczba transakcji: {len(transakcje)}")
print(f"Liczba unikalnych produktow: {len(wynik)}")

print(f"\nSlownik wynikowy: {wynik}")

print("\nWartosc sprzedazy wedlug produktu:")

for produkt, suma in wynik.items():
    print(f"{produkt:12} : {suma:5} zl")

print(f"\nLaczna wartosc sprzedazy: {sum(wynik.values())} zl")

# Weryfikacja wyniku
oczekiwane = {
    "laptop": 5998,
    "mysz": 267,
    "klawiatura": 249
}

print(f"Czy wynik jest poprawny: {wynik == oczekiwane}")
