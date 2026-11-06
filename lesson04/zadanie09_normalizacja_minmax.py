# Lekcja 04 - Zadanie 9: Normalizacja Min-Max

minimum = 50
maksimum = 100

wartosci = [75, 50, 100, 62.5]

print(f"{'Wartość oryginalna':<22} {'Znormalizowana':<18} {'W zakresie [0, 1]'}")
print("-" * 60)

for wartosc in wartosci:
    normalized = (wartosc - minimum) / (maksimum - minimum)

    w_zakresie = 0 <= normalized <= 1

    print(f"{wartosc:<22} {normalized:<18.2f} {w_zakresie}")
