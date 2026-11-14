# Lekcja 07 - Zadanie 12: Walidacja numeru PESEL

# Lista numerow PESEL
pesele = [
    '92041812345',
    '8501015432',
    'abc123',
    '78121698765'
]

# Sprawdzanie poprawnosci formatu
for pesel in pesele:
    if len(pesel) != 11:
        print(
            f"PESEL {pesel}: błędny format "
            f"(długość {len(pesel)})"
        )

    elif not pesel.isdigit():
        print(
            f"PESEL {pesel}: błędny format "
            "(znaki inne niż cyfry)"
        )

    else:
        print(f"PESEL {pesel}: poprawny format")
