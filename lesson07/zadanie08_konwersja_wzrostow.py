# Lekcja 07 - Zadanie 8: Konwersja wzrostow - list comprehension

# Lista wzrostow w centymetrach
wzrosty_cm = [165, 178, 182, 159, 171, 190]

# Konwersja centymetrow na metry
wzrosty_m = [wzrost / 100 for wzrost in wzrosty_cm]

# Wyswietlenie obu list
print(f"Wzrosty w centymetrach: {wzrosty_cm}")
print(f"Wzrosty w metrach: {wzrosty_m}")
