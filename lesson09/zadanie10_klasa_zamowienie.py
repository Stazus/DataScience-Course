# Lekcja 09 - Zadanie 10: Klasa Zamowienie z kompozycja


# Klasa reprezentujaca produkt
class Produkt:
    def __init__(self, nazwa, cena):
        self.nazwa = nazwa
        self.cena = cena


# Klasa reprezentujaca zamowienie
class Zamowienie:
    def __init__(self):
        self.produkty = []

    def dodaj_produkt(self, produkt, ilosc):
        if ilosc <= 0:
            print("Blad: ilosc musi byc dodatnia.")
            return

        if produkt.cena < 0:
            print("Blad: cena nie moze byc ujemna.")
            return

        self.produkty.append((produkt, ilosc))
        print(f"Dodano: {produkt.nazwa} - {ilosc} szt.")

    def laczna_wartosc(self):
        return sum(
            produkt.cena * ilosc
            for produkt, ilosc in self.produkty
        )

    def pokaz_zamowienie(self):
        print("\nSZCZEGOLY ZAMOWIENIA")
        print("=" * 75)

        for numer, (produkt, ilosc) in enumerate(self.produkty, start=1):
            wartosc = produkt.cena * ilosc

            print(
                f"{numer}. {produkt.nazwa} | "
                f"Cena: {produkt.cena:.2f} zl | "
                f"Ilosc: {ilosc} | "
                f"Wartosc: {wartosc:.2f} zl"
            )

        print("-" * 75)
        print(f"Laczna wartosc: {self.laczna_wartosc():.2f} zl")


# Utworzenie 5 produktow
produkty = [
    Produkt("Laptop", 3500),
    Produkt("Monitor", 1200),
    Produkt("Klawiatura", 150),
    Produkt("Mysz", 100),
    Produkt("Sluchawki", 250)
]

# Utworzenie zamowienia
zamowienie = Zamowienie()

print("DODAWANIE PRODUKTOW")
print("=" * 75)

zamowienie.dodaj_produkt(produkty[0], 1)
zamowienie.dodaj_produkt(produkty[1], 2)
zamowienie.dodaj_produkt(produkty[2], 3)
zamowienie.dodaj_produkt(produkty[3], 2)
zamowienie.dodaj_produkt(produkty[4], 1)

# Wyswietlenie zamowienia
zamowienie.pokaz_zamowienie()

# Weryfikacja
oczekiwana_wartosc = 6800
rzeczywista_wartosc = zamowienie.laczna_wartosc()

print("\nWERYFIKACJA")
print("=" * 75)
print(f"Czy zamowienie zawiera 5 produktow: {len(zamowienie.produkty) == 5}")
print(f"Czy laczna wartosc wynosi 6800 zl: {rzeczywista_wartosc == oczekiwana_wartosc}")
print(f"Czy wszystkie elementy sa obiektami Produkt: {all(isinstance(p, Produkt) for p, i in zamowienie.produkty)}")
