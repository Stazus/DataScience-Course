# Lekcja 09 - Zadanie 16: Dziedziczenie wielopoziomowe - Zwierzeta


# Klasa bazowa
class Zwierze:
    def __init__(self, nazwa, wiek):
        self.nazwa = nazwa
        self.wiek = wiek

    def pokaz_info(self):
        print(f"Nazwa: {self.nazwa}")
        print(f"Wiek: {self.wiek} lat")


# Klasa potomna - Ssak
class Ssak(Zwierze):
    def __init__(self, nazwa, wiek, typ_futra):
        super().__init__(nazwa, wiek)
        self.typ_futra = typ_futra

    def pokaz_info(self):
        super().pokaz_info()
        print(f"Typ futra: {self.typ_futra}")


# Klasa potomna - Pies
class Pies(Ssak):
    def __init__(self, nazwa, wiek, typ_futra, rasa):
        super().__init__(nazwa, wiek, typ_futra)
        self.rasa = rasa

    def pokaz_info(self):
        super().pokaz_info()
        print(f"Rasa: {self.rasa}")


# Utworzenie obiektu klasy Pies
pies = Pies("Reksio", 5, "krotkie", "Labrador")


print("DZIEDZICZENIE WIELOPOZIOMOWE - ZWIERZETA")
print("=" * 65)

print("\nINFORMACJE O PSIE")
print("=" * 65)
pies.pokaz_info()


# Dodatkowe obiekty do testowania klas
zwierze = Zwierze("Zwierze testowe", 3)
ssak = Ssak("Kot", 4, "dlugie")


print("\nINFORMACJE O ZWIERZECIU")
print("=" * 65)
zwierze.pokaz_info()

print("\nINFORMACJE O SSAKU")
print("=" * 65)
ssak.pokaz_info()


# Weryfikacja dziedziczenia
print("\nWERYFIKACJA")
print("=" * 65)

print(f"Czy Pies dziedziczy po Ssak: {issubclass(Pies, Ssak)}")
print(f"Czy Ssak dziedziczy po Zwierze: {issubclass(Ssak, Zwierze)}")
print(f"Czy Pies dziedziczy po Zwierze: {issubclass(Pies, Zwierze)}")

print(f"Czy pies jest obiektem Pies: {isinstance(pies, Pies)}")
print(f"Czy pies jest obiektem Ssak: {isinstance(pies, Ssak)}")
print(f"Czy pies jest obiektem Zwierze: {isinstance(pies, Zwierze)}")

print(
    "Czy pies posiada wszystkie atrybuty: "
    f"{all(hasattr(pies, atrybut) for atrybut in ('nazwa', 'wiek', 'typ_futra', 'rasa'))}"
)
