# Lekcja 09 - Zadanie 13: System biblioteki


class Ksiazka:
    def __init__(self, tytul, autor, dostepna=True):
        self.tytul = tytul
        self.autor = autor
        self.dostepna = dostepna

    def __str__(self):
        status = "dostepna" if self.dostepna else "wypozyczona"
        return f"{self.tytul} - {self.autor} ({status})"


class Uzytkownik:
    def __init__(self, imie, wypozyczone_ksiazki=None):
        self.imie = imie
        self.wypozyczone_ksiazki = (
            list(wypozyczone_ksiazki)
            if wypozyczone_ksiazki is not None else []
        )


class Biblioteka:
    def __init__(self, ksiazki=None, uzytkownicy=None):
        self.ksiazki = list(ksiazki) if ksiazki is not None else []
        self.uzytkownicy = (
            list(uzytkownicy) if uzytkownicy is not None else []
        )

    def dodaj_ksiazke(self, ksiazka):
        self.ksiazki.append(ksiazka)

    def zarejestruj_uzytkownika(self, uzytkownik):
        self.uzytkownicy.append(uzytkownik)

    def wypozycz(self, uzytkownik, ksiazka):
        if uzytkownik not in self.uzytkownicy:
            print("Blad: uzytkownik nie jest zarejestrowany.")
            return False

        if ksiazka not in self.ksiazki:
            print("Blad: ksiazka nie nalezy do biblioteki.")
            return False

        if not ksiazka.dostepna:
            print(f"Ksiazka '{ksiazka.tytul}' jest niedostepna.")
            return False

        ksiazka.dostepna = False
        uzytkownik.wypozyczone_ksiazki.append(ksiazka)

        print(f"{uzytkownik.imie} wypozyczyl(a): {ksiazka.tytul}")
        return True

    def zwroc(self, uzytkownik, ksiazka):
        if uzytkownik not in self.uzytkownicy:
            print("Blad: uzytkownik nie jest zarejestrowany.")
            return False

        if ksiazka not in self.ksiazki:
            print("Blad: ksiazka nie nalezy do biblioteki.")
            return False

        if ksiazka not in uzytkownik.wypozyczone_ksiazki:
            print(
                f"Blad: {uzytkownik.imie} nie wypozyczyl(a) "
                f"ksiazki '{ksiazka.tytul}'."
            )
            return False

        uzytkownik.wypozyczone_ksiazki.remove(ksiazka)
        ksiazka.dostepna = True

        print(f"{uzytkownik.imie} zwrocil(a): {ksiazka.tytul}")
        return True

    def raport(self):
        dostepne = sum(ksiazka.dostepna for ksiazka in self.ksiazki)
        wypozyczone = len(self.ksiazki) - dostepne

        print("\nRAPORT BIBLIOTEKI")
        print("=" * 70)
        print(f"Liczba ksiazek: {len(self.ksiazki)}")
        print(f"Ksiazki dostepne: {dostepne}")
        print(f"Ksiazki wypozyczone: {wypozyczone}")
        print(f"Liczba uzytkownikow: {len(self.uzytkownicy)}")

        print("\nWYPOZYCZENIA UZYTKOWNIKOW")
        for uzytkownik in self.uzytkownicy:
            tytuly = [
                ksiazka.tytul
                for ksiazka in uzytkownik.wypozyczone_ksiazki
            ]
            print(f"{uzytkownik.imie}: {tytuly}")


# Utworzenie biblioteki
biblioteka = Biblioteka()

# Utworzenie 10 ksiazek
ksiazki = [
    Ksiazka("Pan Tadeusz", "Adam Mickiewicz"),
    Ksiazka("Lalka", "Boleslaw Prus"),
    Ksiazka("Quo Vadis", "Henryk Sienkiewicz"),
    Ksiazka("Solaris", "Stanislaw Lem"),
    Ksiazka("Wiedzmin", "Andrzej Sapkowski"),
    Ksiazka("Dziady", "Adam Mickiewicz"),
    Ksiazka("Ferdydurke", "Witold Gombrowicz"),
    Ksiazka("Przedwiosnie", "Stefan Zeromski"),
    Ksiazka("Zbrodnia i kara", "Fiodor Dostojewski"),
    Ksiazka("Rok 1984", "George Orwell")
]

for ksiazka in ksiazki:
    biblioteka.dodaj_ksiazke(ksiazka)

# Utworzenie 3 uzytkownikow
jan = Uzytkownik("Jan")
anna = Uzytkownik("Anna")
piotr = Uzytkownik("Piotr")

for uzytkownik in [jan, anna, piotr]:
    biblioteka.zarejestruj_uzytkownika(uzytkownik)


print("SYSTEM ZARZADZANIA BIBLIOTEKA")
print("=" * 70)

print("\nWYPOZYCZENIA")
print("=" * 70)

biblioteka.wypozycz(jan, ksiazki[0])
biblioteka.wypozycz(jan, ksiazki[1])
biblioteka.wypozycz(anna, ksiazki[2])
biblioteka.wypozycz(anna, ksiazki[3])
biblioteka.wypozycz(piotr, ksiazki[4])

print("\nTEST NIEDOSTEPNEJ KSIAZKI")
print("=" * 70)
test_niedostepnej = biblioteka.wypozycz(piotr, ksiazki[0])

print("\nZWROTY")
print("=" * 70)
biblioteka.zwroc(jan, ksiazki[0])
biblioteka.zwroc(anna, ksiazki[2])

print("\nPONOWNE WYPOZYCZENIE")
print("=" * 70)
test_ponownego = biblioteka.wypozycz(piotr, ksiazki[0])

print("\nTEST NIEPRAWIDLOWEGO ZWROTU")
print("=" * 70)
test_zlego_zwrotu = biblioteka.zwroc(jan, ksiazki[4])

# Raport koncowy
biblioteka.raport()

# Weryfikacja
dostepne = sum(ksiazka.dostepna for ksiazka in biblioteka.ksiazki)
wypozyczone = len(biblioteka.ksiazki) - dostepne

print("\nWERYFIKACJA")
print("=" * 70)
print(f"Czy biblioteka ma 10 ksiazek: {len(biblioteka.ksiazki) == 10}")
print(f"Czy zarejestrowano 3 uzytkownikow: {len(biblioteka.uzytkownicy) == 3}")
print(f"Czy wypozyczono 4 ksiazki: {wypozyczone == 4}")
print(f"Czy dostepnych jest 6 ksiazek: {dostepne == 6}")
print(f"Czy zablokowano zajeta ksiazke: {test_niedostepnej is False}")
print(f"Czy ponowne wypozyczenie dziala: {test_ponownego is True}")
print(f"Czy zablokowano bledny zwrot: {test_zlego_zwrotu is False}")
