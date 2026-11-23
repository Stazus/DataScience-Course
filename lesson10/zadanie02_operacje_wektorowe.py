# Lekcja 10 - Zadanie 2: Operacje wektorowe

import numpy as np


# Ceny produktow przed rabatem i po rabacie
before = np.array([100, 250, 75, 320, 180, 450, 90])
after = np.array([80, 200, 60, 280, 150, 400, 75])

# Operacje wektorowe - bez petli
oszczednosci = before - after
procent_rabatu = (oszczednosci / before) * 100
srednia_oszczednosc = np.mean(oszczednosci)

# Zaokraglenie wynikow
oszczednosci = np.round(oszczednosci, 2)
procent_rabatu = np.round(procent_rabatu, 2)
srednia_oszczednosc = np.round(srednia_oszczednosc, 2)

print("OPERACJE WEKTOROWE - ANALIZA RABATOW")
print("=" * 65)

print(f"Ceny przed rabatem: {before}")
print(f"Ceny po rabacie:    {after}")

print("\nOSZCZEDNOSCI")
print("=" * 65)
print(f"Oszczednosci na produktach: {oszczednosci} zl")

print("\nPROCENT RABATU")
print("=" * 65)
print(f"Rabaty procentowe: {procent_rabatu}%")

print("\nPODSUMOWANIE")
print("=" * 65)
print(f"Liczba produktow: {before.size}")
print(f"Srednia oszczednosc: {srednia_oszczednosc:.2f} zl")
print(f"Laczna oszczednosc: {np.sum(oszczednosci):.2f} zl")

# Weryfikacja wynikow
oczekiwane_oszczednosci = np.array([20, 50, 15, 40, 30, 50, 15])
oczekiwane_rabaty = np.array([
    20.00, 20.00, 20.00, 12.50, 16.67, 11.11, 16.67
])

print("\nWERYFIKACJA")
print("=" * 65)
print(f"Czy sa 7 produktow: {before.size == 7}")
print(
    "Czy oszczednosci sa poprawne: "
    f"{np.array_equal(oszczednosci, oczekiwane_oszczednosci)}"
)
print(
    "Czy rabaty procentowe sa poprawne: "
    f"{np.array_equal(procent_rabatu, oczekiwane_rabaty)}"
)
print(f"Czy srednia oszczednosc jest poprawna: {srednia_oszczednosc == 31.43}")
print(f"Czy laczna oszczednosc wynosi 220 zl: {np.sum(oszczednosci) == 220}")
