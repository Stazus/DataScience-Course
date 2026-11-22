# Lekcja 09 - Zadanie 15: Symulator portfela inwestycyjnego


class Akcja:
    def __init__(self, nazwa, cena_kupna, cena_aktualna):
        self.nazwa = nazwa
        self.cena_kupna = cena_kupna
        self.cena_aktualna = cena_aktualna


class Portfel:
    def __init__(self, kapital_poczatkowy, akcje=None):
        self.kapital_poczatkowy = kapital_poczatkowy
        self.gotowka = kapital_poczatkowy
        self.akcje = list(akcje) if akcje is not None else []

    def kup_akcje(self, akcja, ilosc):
        if ilosc <= 0 or akcja.cena_kupna <= 0:
            print("Blad: nieprawidlowa ilosc lub cena.")
            return False

        koszt = akcja.cena_kupna * ilosc

        if koszt > self.gotowka:
            print(f"Brak srodkow na zakup: {akcja.nazwa}")
            return False

        # Pozycja: akcja oraz liczba posiadanych sztuk
        for pozycja in self.akcje:
            if pozycja["akcja"].nazwa == akcja.nazwa:
                if pozycja["akcja"].cena_kupna != akcja.cena_kupna:
                    print("Blad: rozna cena zakupu tej samej akcji.")
                    return False
                pozycja["ilosc"] += ilosc
                break
        else:
            self.akcje.append({"akcja": akcja, "ilosc": ilosc})

        self.gotowka -= koszt
        print(f"Kupiono {ilosc} szt. {akcja.nazwa} za {koszt:.2f} zl")
        return True

    def sprzedaj_akcje(self, akcja, ilosc):
        if ilosc <= 0:
            print("Blad: ilosc musi byc dodatnia.")
            return False

        for pozycja in self.akcje:
            if pozycja["akcja"].nazwa == akcja.nazwa:
                if ilosc > pozycja["ilosc"]:
                    print(f"Za malo akcji: {akcja.nazwa}")
                    return False

                przychod = pozycja["akcja"].cena_aktualna * ilosc
                pozycja["ilosc"] -= ilosc
                self.gotowka += przychod

                if pozycja["ilosc"] == 0:
                    self.akcje.remove(pozycja)

                print(
                    f"Sprzedano {ilosc} szt. {akcja.nazwa} "
                    f"za {przychod:.2f} zl"
                )
                return True

        print(f"Nie posiadasz akcji: {akcja.nazwa}")
        return False

    def aktualizuj_ceny(self, slownik_cen):
        for pozycja in self.akcje:
            akcja = pozycja["akcja"]

            if akcja.nazwa in slownik_cen:
                nowa_cena = slownik_cen[akcja.nazwa]

                if nowa_cena < 0:
                    print(f"Nieprawidlowa cena: {akcja.nazwa}")
                    continue

                akcja.cena_aktualna = nowa_cena

    def wartosc_portfela(self):
        wartosc_akcji = sum(
            pozycja["akcja"].cena_aktualna * pozycja["ilosc"]
            for pozycja in self.akcje
        )

        return self.gotowka + wartosc_akcji

    def zysk_strata(self):
        return self.wartosc_portfela() - self.kapital_poczatkowy

    def raport(self):
        print("\nRAPORT PORTFELA")
        print("=" * 75)

        for pozycja in self.akcje:
            akcja = pozycja["akcja"]
            ilosc = pozycja["ilosc"]
            wartosc = akcja.cena_aktualna * ilosc

            print(
                f"{akcja.nazwa:12} | "
                f"Ilosc: {ilosc:3} | "
                f"Cena: {akcja.cena_aktualna:8.2f} zl | "
                f"Wartosc: {wartosc:10.2f} zl"
            )

        print("-" * 75)
        print(f"Gotowka: {self.gotowka:.2f} zl")
        print(f"Wartosc portfela: {self.wartosc_portfela():.2f} zl")
        print(f"Zysk / strata: {self.zysk_strata():+.2f} zl")


# Utworzenie portfela
portfel = Portfel(kapital_poczatowy := 50000)

# Piec przykladowych akcji
akcje = [
    Akcja("CD Projekt", 150, 150),
    Akcja("PKO BP", 50, 50),
    Akcja("Orlen", 65, 65),
    Akcja("KGHM", 120, 120),
    Akcja("PZU", 45, 45)
]

print("SYMULATOR PORTFELA INWESTYCYJNEGO")
print("=" * 75)
print(f"Kapital poczatkowy: {portfel.kapital_poczatkowy:.2f} zl")

print("\nZAKUP AKCJI")
print("=" * 75)

ilosci = [20, 100, 80, 30, 100]

for akcja, ilosc in zip(akcje, ilosci):
    portfel.kup_akcje(akcja, ilosc)

print("\nAKTUALIZACJA CEN")
print("=" * 75)

nowe_ceny = {
    "CD Projekt": 180,
    "PKO BP": 55,
    "Orlen": 60,
    "KGHM": 140,
    "PZU": 42
}

portfel.aktualizuj_ceny(nowe_ceny)

for akcja in akcje:
    print(f"{akcja.nazwa}: {akcja.cena_aktualna:.2f} zl")

print("\nSPRZEDAZ AKCJI")
print("=" * 75)

portfel.sprzedaj_akcje(akcje[0], 5)
portfel.sprzedaj_akcje(akcje[1], 20)

portfel.raport()

print("\nWERYFIKACJA")
print("=" * 75)

oczekiwana_gotowka = 30700.0
oczekiwana_wartosc = 51000.0
oczekiwany_zysk = 1000.0

print(f"Czy pozostalo 5 pozycji: {len(portfel.akcje) == 5}")
print(
    f"Czy gotowka jest poprawna: "
    f"{abs(portfel.gotowka - oczekiwana_gotowka) < 0.01}"
)
print(
    f"Czy wartosc portfela jest poprawna: "
    f"{abs(portfel.wartosc_portfela() - oczekiwana_wartosc) < 0.01}"
)
print(
    f"Czy zysk jest poprawny: "
    f"{abs(portfel.zysk_strata() - oczekiwany_zysk) < 0.01}"
)
