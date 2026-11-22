# Lekcja 09 - Zadanie 12: Dziedziczenie - FiguraGeometryczna

import math


# Klasa bazowa
class Figura:
    def pole(self):
        raise NotImplementedError(
            "Klasa potomna musi implementowac metode pole()."
        )


# Klasa potomna - Prostokat
class Prostokat(Figura):
    def __init__(self, szerokosc, wysokosc):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc

    def pole(self):
        return self.szerokosc * self.wysokosc


# Klasa potomna - Kolo
class Kolo(Figura):
    def __init__(self, promien):
        self.promien = promien

    def pole(self):
        return math.pi * self.promien ** 2


# Utworzenie listy figur
figury = [
    Prostokat(5, 4),
    Kolo(3),
    Prostokat(10, 2),
    Kolo(5),
    Prostokat(7, 3)
]


# Wyswietlenie wynikow
print("DZIEDZICZENIE - FIGURY GEOMETRYCZNE")
print("=" * 70)

print("\nLISTA FIGUR")
print("=" * 70)

for numer, figura in enumerate(figury, start=1):
    print(
        f"{numer}. {type(figura).__name__} | "
        f"Pole: {figura.pole():.2f}"
    )


# Obliczenie lacznego pola
laczne_pole = sum(figura.pole() for figura in figury)

print("\nPODSUMOWANIE")
print("=" * 70)
print(f"Liczba figur: {len(figury)}")
print(f"Laczne pole figur: {laczne_pole:.2f}")


# Weryfikacja
oczekiwane_pole = 61 + 34 * math.pi

print("\nWERYFIKACJA")
print("=" * 70)

print(f"Czy utworzono 5 figur: {len(figury) == 5}")

print(
    f"Czy wszystkie figury dziedzicza po Figura: "
    f"{all(isinstance(figura, Figura) for figura in figury)}"
)

print(
    f"Czy pole prostokata jest poprawne: "
    f"{figury[0].pole() == 20}"
)

print(
    f"Czy pole kola jest poprawne: "
    f"{math.isclose(figury[1].pole(), 9 * math.pi)}"
)

print(
    f"Czy laczne pole jest poprawne: "
    f"{math.isclose(laczne_pole, oczekiwane_pole)}"
)
