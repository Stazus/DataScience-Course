# Lekcja 06 - Zadanie 5: Operacje na dwóch zbiorach

# Zbiory narzędzi używanych przez analityków
grupa_a = {'python', 'pandas', 'numpy', 'sql', 'tableau'}
grupa_b = {'python', 'r', 'sql', 'ggplot2', 'dplyr'}

# Suma zbiorów
print("SUMA ZBIORÓW")
print(f"Operator |: {grupa_a | grupa_b}")
print(f"Metoda union(): {grupa_a.union(grupa_b)}")

# Iloczyn zbiorów
print("\nILOCZYN ZBIORÓW")
print(f"Operator &: {grupa_a & grupa_b}")
print(f"Metoda intersection(): {grupa_a.intersection(grupa_b)}")

# Różnica zbiorów
print("\nRÓŻNICA ZBIORÓW")
print(f"Operator -: {grupa_a - grupa_b}")
print(f"Metoda difference(): {grupa_a.difference(grupa_b)}")

# Różnica symetryczna
print("\nRÓŻNICA SYMETRYCZNA")
print(f"Operator ^: {grupa_a ^ grupa_b}")
print(f"Metoda symmetric_difference(): {grupa_a.symmetric_difference(grupa_b)}")

# Sprawdzenie rozłączności zbiorów
print("\nROZŁĄCZNOŚĆ ZBIORÓW")
print(f"Czy zbiory są rozłączne: {grupa_a.isdisjoint(grupa_b)}")
