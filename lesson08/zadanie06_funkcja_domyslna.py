# Lekcja 08 - Zadanie 06: Funkcja z wartosciami domyslnymi

# Definicja funkcji
def powitanie(imie, jezyk="polski"):
    """Zwraca powitanie w wybranym jezyku."""

    if jezyk == "polski":
        return f"Cześć, {imie}!"

    elif jezyk == "angielski":
        return f"Hello, {imie}!"

    elif jezyk == "niemiecki":
        return f"Hallo, {imie}!"

    else:
        return "Nieobslugiwany jezyk."


# Wyswietlenie wynikow
print("POWITANIA W TRZECH JEZYKACH")
print("=" * 50)

# Wywolanie z domyslnym jezykiem
print(powitanie("Anna"))

# Wywolanie z jezykiem angielskim
print(powitanie("Anna", "angielski"))

# Wywolanie z jezykiem niemieckim
print(powitanie("Anna", "niemiecki"))
