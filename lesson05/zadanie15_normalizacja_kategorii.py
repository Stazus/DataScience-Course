# Lekcja 05 - Zadanie 15: Normalizacja pojedynczej kategorii

# Dane wejściowe z dwóch różnych źródeł
kat_a = "  Electronics  "
kat_b = "ELECTRONICS"

# Normalizacja kategorii
kat_a_norm = kat_a.strip().lower()
kat_b_norm = kat_b.strip().lower()

# Porównanie znormalizowanych wartości
czy_identyczne = kat_a_norm == kat_b_norm

# Wyświetlanie wyników
print("PRZED NORMALIZACJĄ")
print(f"Kategoria A: '{kat_a}'")
print(f"Kategoria B: '{kat_b}'")

print("\nPO NORMALIZACJI")
print(f"Kategoria A: '{kat_a_norm}'")
print(f"Kategoria B: '{kat_b_norm}'")

print(f"\nCzy kategorie są identyczne: {czy_identyczne}")
