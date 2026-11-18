# Lekcja 08 - Zadanie 02: Konwerter jednostek

# Definicje funkcji
def celsius_to_fahrenheit(c):
    """Konwertuje stopnie Celsjusza na Fahrenheita."""
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f):
    """Konwertuje stopnie Fahrenheita na Celsjusza."""
    return (f - 32) * 5 / 9


def celsius_to_kelvin(c):
    """Konwertuje stopnie Celsjusza na Kelviny."""
    return c + 273.15


# Dane wejsciowe
temperatury = [0, 10, 20, 30, 37, 100]

# Naglowek tabeli
print("KONWERTER JEDNOSTEK TEMPERATURY")
print("=" * 40)
print(f"{'°C':>10} {'°F':>10} {'K':>10}")
print("-" * 40)

# Konwersja wszystkich temperatur
for c in temperatury:
    f = celsius_to_fahrenheit(c)
    k = celsius_to_kelvin(c)
    c_powrot = fahrenheit_to_celsius(f)

    print(f"{c_powrot:>10.2f} {f:>10.2f} {k:>10.2f}")

print("=" * 40)
