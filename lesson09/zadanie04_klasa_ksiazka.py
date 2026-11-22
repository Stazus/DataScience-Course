# Lekcja 09 - Zadanie 4: Klasa Ksiazka


class Ksiazka:
    def __init__(self, tytul, autor, rok_wydania, liczba_stron):
        self.tytul = tytul
        self.autor = autor
        self.rok_wydania = rok_wydania
        self.liczba_stron = liczba_stron

    def __str__(self):
        return (
            f"Tytul: {self.tytul} | "
            f"Autor: {self.autor} | "
            f"Rok wydania: {self.rok_wydania} | "
            f"Liczba stron: {self.liczba_stron}"
        )


# Utworzenie listy 5 ksiazek
ksiazki = [
    Ksiazka("Pan Tadeusz", "Adam Mickiewicz", 1834, 340),
    Ksiazka("Lalka", "Boleslaw Prus", 1890, 680),
    Ksiazka("Quo Vadis", "Henryk Sienkiewicz", 1896, 560),
    Ksiazka("Solaris", "Stanislaw Lem", 1961, 220),
    Ksiazka("Wiedzmin", "Andrzej Sapkowski", 1990, 320)
]


# Wyswietlenie ksiazek
print("LISTA KSIAZEK")
print("=" * 90)

for numer, ksiazka in enumerate(ksiazki, start=1):
    print(f"{numer}. {ksiazka}")


# Weryfikacja
print("\nWERYFIKACJA")
print("=" * 90)

print(f"Liczba ksiazek: {len(ksiazki)}")
print(f"Czy utworzono 5 ksiazek: {len(ksiazki) == 5}")

print(
    f"Czy wszystkie obiekty sa klasy Ksiazka: "
    f"{all(isinstance(ksiazka, Ksiazka) for ksiazka in ksiazki)}"
)

print(
    f"Czy metoda __str__ zwraca tekst: "
    f"{all(isinstance(str(ksiazka), str) for ksiazka in ksiazki)}"
)

print(
    f"Laczna liczba stron: "
    f"{sum(ksiazka.liczba_stron for ksiazka in ksiazki)}"
)
