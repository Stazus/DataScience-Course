# Lekcja 06 - Zadanie 16: Analiza sprzedazy z kluczem-krotka

# Dane sprzedazy kwartalnej
sprzedaz = {
    (2024, 'Q1'): 120_000,
    (2024, 'Q2'): 145_000,
    (2024, 'Q3'): 138_000,
    (2024, 'Q4'): 167_000,
    (2025, 'Q1'): 130_000,
    (2025, 'Q2'): 155_000,
    (2025, 'Q3'): 149_000
}

# Podstawowe statystyki sprzedazy
calkowita = sum(sprzedaz.values())
maksimum = max(sprzedaz.values())
minimum = min(sprzedaz.values())

print("STATYSTYKI SPRZEDAZY")
print(f"Calkowita sprzedaz: {calkowita} zl")
print(f"Najwyzsza sprzedaz: {maksimum} zl")
print(f"Najnizsza sprzedaz: {minimum} zl")

# Znalezienie kwartalu z najwyzsza sprzedaza
najlepszy_kwartal = max(sprzedaz, key=sprzedaz.get)

# Rozpakowanie krotki
rok_max, kw_max = najlepszy_kwartal

print(f"\nNajwyzsza sprzedaz: {rok_max} {kw_max} - {sprzedaz[najlepszy_kwartal]}")

# Sortowanie kluczy wedlug wartosci malejaco
ranking = sorted(sprzedaz, key=sprzedaz.get, reverse=True)

# Trzy najlepsze kwartaly
print("\nTOP 3 KWARTALY")
print(f"1. {ranking[0]}: {sprzedaz[ranking[0]]} zl")
print(f"2. {ranking[1]}: {sprzedaz[ranking[1]]} zl")
print(f"3. {ranking[2]}: {sprzedaz[ranking[2]]} zl")

# Zbior unikalnych lat
klucze = list(sprzedaz.keys())

lata = {
    klucze[0][0],
    klucze[1][0],
    klucze[2][0],
    klucze[3][0],
    klucze[4][0],
    klucze[5][0],
    klucze[6][0]
}

print(f"\nUnikalne lata: {lata}")
print(f"Liczba unikalnych lat: {len(lata)}")
