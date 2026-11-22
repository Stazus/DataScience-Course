# Lekcja 09 - Zadanie 7: Klasa Pracownik


class Pracownik:
    def __init__(self, imie, stanowisko, pensja):
        self.imie = imie
        self.stanowisko = stanowisko
        self.pensja = pensja

    def podwyzka(self, procent):
        if procent < 0:
            print("Blad: procent podwyzki nie moze byc ujemny.")
            return

        stara_pensja = self.pensja
        self.pensja *= 1 + procent / 100

        print(
            f"{self.imie}: podwyzka {procent}% | "
            f"{stara_pensja:.2f} zl -> {self.pensja:.2f} zl"
        )

    def __str__(self):
        return (
            f"Pracownik: {self.imie} | "
            f"Stanowisko: {self.stanowisko} | "
            f"Pensja: {self.pensja:.2f} zl"
        )


# Utworzenie 3 pracownikow
pracownicy = [
    Pracownik("Jan", "Python Developer", 8000),
    Pracownik("Anna", "Data Scientist", 10000),
    Pracownik("Piotr", "DevOps Engineer", 9000)
]

# Procenty podwyzek
podwyzki = [10, 15, 20]

print("STAN POCZATKOWY")
print("=" * 70)

for pracownik in pracownicy:
    print(pracownik)


print("\nPRZYZNAWANIE PODWYZEK")
print("=" * 70)

for pracownik, procent in zip(pracownicy, podwyzki):
    pracownik.podwyzka(procent)


print("\nSTAN KONCOWY")
print("=" * 70)

for pracownik in pracownicy:
    print(pracownik)


# Weryfikacja wynikow
oczekiwane_pensje = [8800, 11500, 10800]

print("\nWERYFIKACJA")
print("=" * 70)

for pracownik, oczekiwana in zip(pracownicy, oczekiwane_pensje):
    poprawny = abs(pracownik.pensja - oczekiwana) < 0.000001
    print(f"{pracownik.imie}: {poprawny}")

wszystkie_poprawne = all(
    abs(pracownik.pensja - oczekiwana) < 0.000001
    for pracownik, oczekiwana in zip(pracownicy, oczekiwane_pensje)
)

print(f"\nCzy utworzono 3 pracownikow: {len(pracownicy) == 3}")
print(f"Czy wszystkie podwyzki sa poprawne: {wszystkie_poprawne}")
