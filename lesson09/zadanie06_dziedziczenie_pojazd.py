# Lekcja 09 - Zadanie 6: Dziedziczenie - Pojazd i Samochod


# Klasa bazowa
class Pojazd:
    def __init__(self, marka, model, rok):
        self.marka = marka
        self.model = model
        self.rok = rok

    def pokaz_info(self):
        print(f"Marka: {self.marka}")
        print(f"Model: {self.model}")
        print(f"Rok produkcji: {self.rok}")


# Klasa potomna
class Samochod(Pojazd):
    def __init__(self, marka, model, rok, liczba_drzwi):
        super().__init__(marka, model, rok)
        self.liczba_drzwi = liczba_drzwi

    def pokaz_info(self):
        super().pokaz_info()
        print(f"Liczba drzwi: {self.liczba_drzwi}")


# Utworzenie obiektu klasy bazowej
pojazd = Pojazd("Yamaha", "MT-07", 2022)

# Utworzenie obiektow klasy potomnej
samochod1 = Samochod("Toyota", "Corolla", 2020, 5)
samochod2 = Samochod("BMW", "320d", 2021, 4)
samochod3 = Samochod("Volkswagen", "Golf", 2019, 5)

samochody = [samochod1, samochod2, samochod3]


# Wyswietlenie pojazdu
print("KLASA BAZOWA - POJAZD")
print("=" * 55)

pojazd.pokaz_info()


# Wyswietlenie samochodow
print("\nKLASA POTOMNA - SAMOCHOD")
print("=" * 55)

for numer, samochod in enumerate(samochody, start=1):
    print(f"\nSamochod {numer}:")
    samochod.pokaz_info()
    print("-" * 55)


# Weryfikacja dziedziczenia
print("\nWERYFIKACJA")
print("=" * 55)

print(
    f"Czy Samochod dziedziczy po Pojazd: "
    f"{issubclass(Samochod, Pojazd)}"
)

print(
    f"Czy samochod1 jest obiektem Samochod: "
    f"{isinstance(samochod1, Samochod)}"
)

print(
    f"Czy samochod1 jest rowniez Pojazd: "
    f"{isinstance(samochod1, Pojazd)}"
)

print(
    f"Czy samochod1 ma atrybut liczba_drzwi: "
    f"{hasattr(samochod1, 'liczba_drzwi')}"
)

print(
    f"Czy utworzono 3 samochody: "
    f"{len(samochody) == 3}"
)
