# Lekcja 09 - Zadanie 19: Gra RPG z klasami postaci


class Postac:
    def __init__(self, imie, hp, atak, obrona):
        self.imie = imie
        self.hp = hp
        self.max_hp = hp
        self.atak = atak
        self.obrona = obrona

    def czy_zyje(self):
        return self.hp > 0

    def otrzymaj_obrazenia(self, obrazenia):
        self.hp = max(0, self.hp - obrazenia)

    def atakuj(self, cel):
        if not self.czy_zyje() or not cel.czy_zyje():
            print("Atak niemozliwy - jedna z postaci nie zyje.")
            return

        obrazenia = max(1, self.atak - cel.obrona)
        cel.otrzymaj_obrazenia(obrazenia)

        print(
            f"{self.imie} atakuje {cel.imie} | "
            f"Obrazenia: {obrazenia} | "
            f"HP celu: {cel.hp}"
        )

    def leczenie(self, punkty):
        if punkty <= 0 or not self.czy_zyje():
            print(f"{self.imie}: leczenie niemozliwe.")
            return

        stare_hp = self.hp
        self.hp = min(self.max_hp, self.hp + punkty)

        print(
            f"{self.imie} odzyskuje {self.hp - stare_hp} HP | "
            f"Aktualne HP: {self.hp}"
        )

    def __str__(self):
        return (
            f"{self.__class__.__name__}: {self.imie} | "
            f"HP: {self.hp}/{self.max_hp} | "
            f"Atak: {self.atak} | Obrona: {self.obrona}"
        )


class Wojownik(Postac):
    def __init__(self, imie, hp, atak, obrona):
        super().__init__(imie, hp, atak + 5, obrona)


class Mag(Postac):
    def rzuc_czar(self, cel, moc=20):
        if not self.czy_zyje() or not cel.czy_zyje():
            print("Czar niemozliwy - jedna z postaci nie zyje.")
            return

        obrazenia = max(1, moc - cel.obrona // 2)
        cel.otrzymaj_obrazenia(obrazenia)

        print(
            f"{self.imie} rzuca czar na {cel.imie} | "
            f"Obrazenia magiczne: {obrazenia} | "
            f"HP celu: {cel.hp}"
        )


class Lucznik(Postac):
    def __init__(self, imie, hp, atak, obrona, szybkosc=2):
        super().__init__(imie, hp, atak, obrona)
        self.szybkosc = szybkosc

    def atakuj(self, cel):
        print(f"{self.imie} wykonuje {self.szybkosc} szybkie ataki!")

        for numer in range(self.szybkosc):
            if not cel.czy_zyje():
                break

            print(f"Strzal {numer + 1}:")
            super().atakuj(cel)


# Utworzenie trzech postaci
wojownik = Wojownik("Aragorn", 120, 20, 8)
mag = Mag("Gandalf", 90, 12, 4)
lucznik = Lucznik("Legolas", 100, 15, 5)

postacie = [wojownik, mag, lucznik]


print("GRA RPG - WALKA TRZECH POSTACI")
print("=" * 75)

print("\nSTAN POCZATKOWY")
print("=" * 75)

for postac in postacie:
    print(postac)


print("\nRUNDA 1")
print("=" * 75)

wojownik.atakuj(mag)
mag.rzuc_czar(lucznik)
lucznik.atakuj(wojownik)


print("\nRUNDA 2")
print("=" * 75)

wojownik.atakuj(lucznik)
mag.atakuj(wojownik)
lucznik.atakuj(mag)


print("\nLECZENIE")
print("=" * 75)

wojownik.leczenie(15)
mag.leczenie(20)
lucznik.leczenie(10)


print("\nSTAN KONCOWY")
print("=" * 75)

for postac in postacie:
    print(postac)


print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy utworzono 3 postacie: {len(postacie) == 3}")
print(f"Czy Wojownik dziedziczy po Postac: {isinstance(wojownik, Postac)}")
print(f"Czy Mag dziedziczy po Postac: {isinstance(mag, Postac)}")
print(f"Czy Lucznik dziedziczy po Postac: {isinstance(lucznik, Postac)}")
print(f"Czy Wojownik ma zwiekszony atak: {wojownik.atak == 25}")
print(f"Czy Lucznik ma zwiekszona szybkosc: {lucznik.szybkosc == 2}")

oczekiwane_hp = [117, 67, 72]

for postac, oczekiwane in zip(postacie, oczekiwane_hp):
    print(f"{postac.imie} - poprawne HP: {postac.hp == oczekiwane}")

print(
    "Czy wszystkie postacie zyja: "
    f"{all(postac.czy_zyje() for postac in postacie)}"
)
