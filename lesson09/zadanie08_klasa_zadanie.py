# Lekcja 09 - Zadanie 8: Klasa Zadanie (TODO list)


class Zadanie:
    def __init__(self, opis, status="do zrobienia"):
        self.opis = opis
        self.status = status

    def oznacz_jako_zrobione(self):
        self.status = "zrobione"

    def __str__(self):
        return f"Zadanie: {self.opis} | Status: {self.status}"


# Utworzenie listy 5 zadan
zadania = [
    Zadanie("Ukonczyc lekcje Python"),
    Zadanie("Wykonac zadania domowe"),
    Zadanie("Przeslac kod na GitHub"),
    Zadanie("Powtorzyc programowanie obiektowe"),
    Zadanie("Przygotowac sie do kolejnej lekcji")
]


print("LISTA ZADAN - STAN POCZATKOWY")
print("=" * 75)

for numer, zadanie in enumerate(zadania, start=1):
    print(f"{numer}. {zadanie}")


# Oznaczenie wybranych zadan jako wykonane
zadania[0].oznacz_jako_zrobione()
zadania[1].oznacz_jako_zrobione()
zadania[2].oznacz_jako_zrobione()


print("\nLISTA ZADAN - PO AKTUALIZACJI")
print("=" * 75)

for numer, zadanie in enumerate(zadania, start=1):
    print(f"{numer}. {zadanie}")


# Podsumowanie
liczba_zrobionych = sum(
    zadanie.status == "zrobione"
    for zadanie in zadania
)

liczba_do_zrobienia = sum(
    zadanie.status == "do zrobienia"
    for zadanie in zadania
)

print("\nPODSUMOWANIE")
print("=" * 75)

print(f"Liczba wszystkich zadan: {len(zadania)}")
print(f"Liczba zrobionych: {liczba_zrobionych}")
print(f"Liczba do zrobienia: {liczba_do_zrobienia}")


# Weryfikacja
print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy utworzono 5 zadan: {len(zadania) == 5}")
print(f"Czy 3 zadania sa zrobione: {liczba_zrobionych == 3}")
print(f"Czy 2 zadania pozostaly: {liczba_do_zrobienia == 2}")
print(
    "Czy wszystkie statusy sa poprawne:",
    [zadanie.status for zadanie in zadania]
    == ["zrobione"] * 3 + ["do zrobienia"] * 2
)
