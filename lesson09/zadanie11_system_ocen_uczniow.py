# Lekcja 09 - Zadanie 11: System ocen uczniow


class Uczen:
    def __init__(self, imie, oceny=None):
        self.imie = imie
        self.oceny = list(oceny) if oceny is not None else []

    def srednia(self):
        if not self.oceny:
            return 0.0

        return sum(self.oceny) / len(self.oceny)

    def __str__(self):
        return (
            f"Uczen: {self.imie} | "
            f"Oceny: {self.oceny} | "
            f"Srednia: {self.srednia():.2f}"
        )


class Klasa:
    def __init__(self, nazwa, uczniowie=None):
        self.nazwa = nazwa
        self.uczniowie = (
            list(uczniowie) if uczniowie is not None else []
        )

    def dodaj_ucznia(self, uczen):
        self.uczniowie.append(uczen)

    def srednia_klasy(self):
        wszystkie_oceny = [
            ocena
            for uczen in self.uczniowie
            for ocena in uczen.oceny
        ]

        if not wszystkie_oceny:
            return 0.0

        return sum(wszystkie_oceny) / len(wszystkie_oceny)

    def najlepszy_uczen(self):
        uczniowie_z_ocenami = [
            uczen for uczen in self.uczniowie
            if uczen.oceny
        ]

        if not uczniowie_z_ocenami:
            return None

        return max(
            uczniowie_z_ocenami,
            key=lambda uczen: uczen.srednia()
        )


# Utworzenie klasy
klasa = Klasa("3A")

# Utworzenie 5 uczniow
uczniowie = [
    Uczen("Jan", [4, 5, 3]),
    Uczen("Anna", [5, 5, 4.5]),
    Uczen("Piotr", [3, 4, 3.5]),
    Uczen("Maria", [5, 4, 5]),
    Uczen("Tomasz", [4, 3, 4])
]

# Dodanie uczniow do klasy
for uczen in uczniowie:
    klasa.dodaj_ucznia(uczen)


# Wyswietlenie uczniow
print("SYSTEM OCEN UCZNIOW")
print("=" * 70)
print(f"Klasa: {klasa.nazwa}")
print(f"Liczba uczniow: {len(klasa.uczniowie)}")

print("\nLISTA UCZNIOW")
print("=" * 70)

for numer, uczen in enumerate(klasa.uczniowie, start=1):
    print(f"{numer}. {uczen}")


# Statystyki
najlepszy = klasa.najlepszy_uczen()

print("\nSTATYSTYKI KLASY")
print("=" * 70)
print(f"Srednia klasy: {klasa.srednia_klasy():.2f}")

if najlepszy is not None:
    print(f"Najlepszy uczen: {najlepszy.imie}")
    print(f"Srednia najlepszego ucznia: {najlepszy.srednia():.2f}")


# Weryfikacja
wszystkie_oceny = [
    ocena
    for uczen in uczniowie
    for ocena in uczen.oceny
]

oczekiwana_srednia = sum(wszystkie_oceny) / len(wszystkie_oceny)

print("\nWERYFIKACJA")
print("=" * 70)
print(f"Czy utworzono 5 uczniow: {len(klasa.uczniowie) == 5}")
print(
    f"Czy srednia klasy jest poprawna: "
    f"{abs(klasa.srednia_klasy() - oczekiwana_srednia) < 0.000001}"
)
print(f"Czy najlepszym uczniem jest Anna: {najlepszy.imie == 'Anna'}")
print(f"Czy najlepsza srednia wynosi 4.83: {round(najlepszy.srednia(), 2) == 4.83}")
