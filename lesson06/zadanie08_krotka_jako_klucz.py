# Lekcja 06 - Zadanie 8: Krotka jako klucz slownika

# Slownik sprzedazy kwartalnej
sprzedaz = {
    (2024, 'Q1'): 120_000,
    (2024, 'Q2'): 140_000,
    (2024, 'Q3'): 135_000,
    (2024, 'Q4'): 160_000
}

# Wyswietlenie sprzedazy w drugim kwartale 2024
print(f"Sprzedaż 2024 Q2: {sprzedaz[(2024, 'Q2')]} zł")

# Dodanie nowego kwartalu
sprzedaz[(2025, 'Q1')] = 130_000

# Obliczenie statystyk sprzedazy
maksimum = max(sprzedaz.values())
minimum = min(sprzedaz.values())
laczna_sprzedaz = sum(sprzedaz.values())

# Liczba kwartalow
liczba_kwartalow = len(sprzedaz)

# Wyswietlanie wynikow
print(f"Najwyższa sprzedaż: {maksimum} zł")
print(f"Najniższa sprzedaż: {minimum} zł")
print(f"Łączna sprzedaż: {laczna_sprzedaz} zł")
print(f"Liczba kwartałów: {liczba_kwartalow}")
