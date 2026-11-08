# Lekcja 05 - Zadanie 16: Raport w tabeli ASCII

# Dane trzech eksperymentów
e1 = ["Exp_01", 0.85, 1.23]
e2 = ["Exp_02", 0.89, 4.56]
e3 = ["Exp_03", 0.87, 7.89]

# Separator tabeli
separator = "=" * 44

# Nagłówek
print(separator)
print(f"{'Experiment':<16}{'Accuracy':>12}{'Time (s)':>12}")
print(separator)

# Wiersze z wynikami eksperymentów
print(f"{e1[0]:<16}{e1[1]:>12.2%}{e1[2]:>12.2f}")
print(f"{e2[0]:<16}{e2[1]:>12.2%}{e2[2]:>12.2f}")
print(f"{e3[0]:<16}{e3[1]:>12.2%}{e3[2]:>12.2f}")

# Zakończenie tabeli
print(separator)
