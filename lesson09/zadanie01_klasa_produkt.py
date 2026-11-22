# Lekcja 09 - Zadanie 1: Tworzenie klasy Produkt


class Produkt:
    def __init__(self, nazwa, cena, ilosc_w_magazynie):
        self.nazwa = nazwa
        self.cena = cena
        self.ilosc_w_magazynie = ilosc_w_magazynie

    def pokaz_info(self):
        print(f"Produkt: {self.nazwa}")
        print(f"Cena: {self.cena:.2f} zl")
        print(f"Ilosc w magazynie: {self.ilosc_w_magazynie}")

    def sprzedaj(self, ilosc):
        if ilosc <= 0:
            print("Ilosc musi byc dodatnia.")
        elif ilosc > self.ilosc_w_magazynie:
            print(f"Brak wystarczajacej ilosci: {self.nazwa}")
        else:
            self.ilosc_w_magazynie -= ilosc
            print(f"Sprzedano {ilosc} szt. produktu {self.nazwa}")

    def dostawa(self, ilosc):
        if ilosc <= 0:
            print("Ilosc musi byc dodatnia.")
        else:
            self.ilosc_w_magazynie += ilosc
            print(f"Dostarczono {ilosc} szt. produktu {self.nazwa}")


# Tworzenie trzech obiektow
produkty = [
    Produkt("Laptop", 3500, 10),
    Produkt("Monitor", 1200, 15),
    Produkt("Klawiatura", 150, 30)
]

print("STAN POCZATKOWY")
print("=" * 50)

for produkt in produkty:
    produkt.pokaz_info()
    print("-" * 50)


print("\nSPRZEDAZ")
print("=" * 50)

produkty[0].sprzedaj(3)
produkty[1].sprzedaj(5)
produkty[2].sprzedaj(10)


print("\nDOSTAWA")
print("=" * 50)

produkty[0].dostawa(5)
produkty[1].dostawa(10)
produkty[2].dostawa(20)


print("\nSTAN KONCOWY")
print("=" * 50)

for produkt in produkty:
    produkt.pokaz_info()
    print("-" * 50)


print("\nWERYFIKACJA")
print("=" * 50)

oczekiwane_stany = [12, 20, 40]

for produkt, oczekiwany in zip(produkty, oczekiwane_stany):
    print(
        f"{produkt.nazwa}: "
        f"{produkt.ilosc_w_magazynie == oczekiwany}"
    )
