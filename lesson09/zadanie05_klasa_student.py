# Lekcja 09 - Zadanie 5: Klasa Student


class Student:
    def __init__(self, imie, numer_indeksu, oceny=None):
        self.imie = imie
        self.numer_indeksu = numer_indeksu
        self.oceny = list(oceny) if oceny is not None else []

    def dodaj_ocene(self, ocena):
        if ocena in (2, 3, 3.5, 4, 4.5, 5):
            self.oceny.append(ocena)
            print(f"Dodano ocene {ocena} dla studenta {self.imie}")
        else:
            print(f"Nieprawidlowa ocena: {ocena}")

    def srednia(self):
        if not self.oceny:
            return 0.0

        return sum(self.oceny) / len(self.oceny)

    def __str__(self):
        return (
            f"Student: {self.imie} | "
            f"Numer indeksu: {self.numer_indeksu} | "
            f"Oceny: {self.oceny} | "
            f"Srednia: {self.srednia():.2f}"
        )


# Utworzenie trzech studentow
student1 = Student("Jan", 10001)
student2 = Student("Anna", 10002)
student3 = Student("Piotr", 10003)

studenci = [student1, student2, student3]

# Dodawanie ocen
print("DODAWANIE OCEN")
print("=" * 70)

student1.dodaj_ocene(4)
student1.dodaj_ocene(5)
student1.dodaj_ocene(3)

student2.dodaj_ocene(5)
student2.dodaj_ocene(4.5)
student2.dodaj_ocene(5)

student3.dodaj_ocene(3)
student3.dodaj_ocene(3.5)
student3.dodaj_ocene(4)

# Wyswietlenie studentow
print("\nLISTA STUDENTOW")
print("=" * 70)

for student in studenci:
    print(student)

# Podsumowanie
print("\nPODSUMOWANIE")
print("=" * 70)

for student in studenci:
    print(
        f"{student.imie}: "
        f"liczba ocen = {len(student.oceny)}, "
        f"srednia = {student.srednia():.2f}"
    )

# Weryfikacja
print("\nWERYFIKACJA")
print("=" * 70)

oczekiwane_srednie = [4.0, 14.5 / 3, 3.5]

for student, oczekiwana in zip(studenci, oczekiwane_srednie):
    print(
        f"{student.imie}: "
        f"{abs(student.srednia() - oczekiwana) < 0.000001}"
    )

print(
    f"\nCzy utworzono 3 studentow: "
    f"{len(studenci) == 3}"
)

print(
    f"Czy kazdy student ma 3 oceny: "
    f"{all(len(student.oceny) == 3 for student in studenci)}"
)

print(
    f"Czy wszystkie srednie sa poprawne: "
    f"{all(abs(student.srednia() - oczekiwana) < 0.000001 for student, oczekiwana in zip(studenci, oczekiwane_srednie))}"
)
