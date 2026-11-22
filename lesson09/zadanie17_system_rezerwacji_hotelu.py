# Lekcja 09 - Zadanie 17: System rezerwacji hotelu

from datetime import date


class Pokoj:
    def __init__(self, numer, typ, cena_za_noc, zajety=False):
        self.numer = numer
        self.typ = typ
        self.cena_za_noc = cena_za_noc
        self.zajety = zajety

    def __str__(self):
        status = "zajety" if self.zajety else "wolny"
        return (
            f"Pokoj {self.numer} | Typ: {self.typ} | "
            f"Cena: {self.cena_za_noc:.2f} zl/noc | Status: {status}"
        )


class Rezerwacja:
    def __init__(self, pokoj, data_od, data_do, gosc):
        self.pokoj = pokoj
        self.data_od = data_od
        self.data_do = data_do
        self.gosc = gosc

    def liczba_nocy(self):
        return (self.data_do - self.data_od).days

    def koszt(self):
        return self.liczba_nocy() * self.pokoj.cena_za_noc


class Hotel:
    def __init__(self, pokoje=None, rezerwacje=None):
        self.pokoje = list(pokoje) if pokoje is not None else []
        self.rezerwacje = (
            list(rezerwacje) if rezerwacje is not None else []
        )

    def dodaj_pokoj(self, pokoj):
        if any(p.numer == pokoj.numer for p in self.pokoje):
            print(f"Blad: pokoj {pokoj.numer} juz istnieje.")
            return False

        self.pokoje.append(pokoj)
        return True

    def rezerwuj(self, numer_pokoju, gosc, data_od, data_do):
        pokoj = next(
            (p for p in self.pokoje if p.numer == numer_pokoju),
            None
        )

        if pokoj is None:
            print(f"Blad: pokoj {numer_pokoju} nie istnieje.")
            return False

        if pokoj.zajety:
            print(f"Blad: pokoj {numer_pokoju} jest juz zajety.")
            return False

        try:
            poczatek = date.fromisoformat(data_od)
            koniec = date.fromisoformat(data_do)
        except (ValueError, TypeError):
            print("Blad: nieprawidlowy format daty. Uzyj RRRR-MM-DD.")
            return False

        if koniec <= poczatek:
            print("Blad: data wyjazdu musi byc pozniejsza.")
            return False

        rezerwacja = Rezerwacja(pokoj, poczatek, koniec, gosc)

        self.rezerwacje.append(rezerwacja)
        pokoj.zajety = True

        print(
            f"Zarezerwowano pokoj {pokoj.numer} dla {gosc} | "
            f"{rezerwacja.liczba_nocy()} nocy | "
            f"Koszt: {rezerwacja.koszt():.2f} zl"
        )
        return True

    def wolne_pokoje(self):
        return [pokoj for pokoj in self.pokoje if not pokoj.zajety]

    def przychod(self):
        return sum(rezerwacja.koszt() for rezerwacja in self.rezerwacje)


# Utworzenie hotelu
hotel = Hotel()

# Dodanie 10 pokoi
dane_pokoi = [
    (101, "jednoosobowy", 200),
    (102, "jednoosobowy", 200),
    (103, "dwuosobowy", 300),
    (104, "dwuosobowy", 300),
    (105, "dwuosobowy", 350),
    (106, "apartament", 500),
    (107, "apartament", 550),
    (108, "jednoosobowy", 220),
    (109, "dwuosobowy", 320),
    (110, "apartament", 600)
]

for numer, typ, cena in dane_pokoi:
    hotel.dodaj_pokoj(Pokoj(numer, typ, cena))


print("SYSTEM REZERWACJI HOTELU")
print("=" * 75)

print("\nLISTA POKOI - STAN POCZATKOWY")
print("=" * 75)

for pokoj in hotel.pokoje:
    print(pokoj)


# Symulacja 5 rezerwacji
print("\nREZERWACJE")
print("=" * 75)

hotel.rezerwuj(101, "Jan Kowalski", "2026-12-01", "2026-12-04")
hotel.rezerwuj(103, "Anna Nowak", "2026-12-02", "2026-12-07")
hotel.rezerwuj(105, "Piotr Wisniewski", "2026-12-05", "2026-12-08")
hotel.rezerwuj(106, "Maria Zielinska", "2026-12-10", "2026-12-12")
hotel.rezerwuj(110, "Tomasz Lewandowski", "2026-12-15", "2026-12-20")


print("\nTEST ZAJETEGO POKOJU")
print("=" * 75)

test_zajetego = hotel.rezerwuj(
    101, "Adam Testowy", "2026-12-20", "2026-12-22"
)


print("\nWOLNE POKOJE")
print("=" * 75)

for pokoj in hotel.wolne_pokoje():
    print(pokoj)


print("\nRAPORT REZERWACJI")
print("=" * 75)

for numer, rezerwacja in enumerate(hotel.rezerwacje, start=1):
    print(
        f"{numer}. Gosc: {rezerwacja.gosc} | "
        f"Pokoj: {rezerwacja.pokoj.numer} | "
        f"Noce: {rezerwacja.liczba_nocy()} | "
        f"Koszt: {rezerwacja.koszt():.2f} zl"
    )


print("\nPODSUMOWANIE")
print("=" * 75)

print(f"Liczba pokoi: {len(hotel.pokoje)}")
print(f"Liczba rezerwacji: {len(hotel.rezerwacje)}")
print(f"Liczba zajetych pokoi: {sum(p.zajety for p in hotel.pokoje)}")
print(f"Liczba wolnych pokoi: {len(hotel.wolne_pokoje())}")
print(f"Laczny przychod: {hotel.przychod():.2f} zl")


print("\nWERYFIKACJA")
print("=" * 75)

oczekiwany_przychod = 7150.0

print(f"Czy hotel ma 10 pokoi: {len(hotel.pokoje) == 10}")
print(f"Czy wykonano 5 rezerwacji: {len(hotel.rezerwacje) == 5}")
print(f"Czy zajetych jest 5 pokoi: {sum(p.zajety for p in hotel.pokoje) == 5}")
print(f"Czy wolnych jest 5 pokoi: {len(hotel.wolne_pokoje()) == 5}")
print(f"Czy zablokowano zajety pokoj: {test_zajetego is False}")
print(f"Czy przychod jest poprawny: {hotel.przychod() == oczekiwany_przychod}")
