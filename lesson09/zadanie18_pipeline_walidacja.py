# Lekcja 09 - Zadanie 18: Pipeline z walidacja danych

import math


class WalidatorZakresu:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def sprawdz(self, dane):
        for indeks, wartosc in enumerate(dane):
            if isinstance(wartosc, bool) or not isinstance(wartosc, (int, float)):
                return False, f"Indeks {indeks}: wartosc nie jest liczba."

            if not math.isfinite(wartosc):
                return False, f"Indeks {indeks}: wartosc nie jest skonczona."

            if not self.min <= wartosc <= self.max:
                return False, (
                    f"Indeks {indeks}: {wartosc} poza zakresem "
                    f"[{self.min}, {self.max}]."
                )

        return True, "Wszystkie wartosci mieszcza sie w zakresie."


class WalidatorTypu:
    def __init__(self, typ):
        self.typ = typ

    def sprawdz(self, dane):
        for indeks, wartosc in enumerate(dane):
            if type(wartosc) is not self.typ:
                return False, (
                    f"Indeks {indeks}: oczekiwano {self.typ.__name__}, "
                    f"otrzymano {type(wartosc).__name__}."
                )

        return True, f"Wszystkie wartosci maja typ {self.typ.__name__}."


class WalidatorBrakow:
    def sprawdz(self, dane):
        for indeks, wartosc in enumerate(dane):
            if wartosc is None:
                return False, f"Indeks {indeks}: wykryto None."

            if isinstance(wartosc, float) and math.isnan(wartosc):
                return False, f"Indeks {indeks}: wykryto NaN."

        return True, "Nie wykryto brakujacych wartosci."


class Pipeline:
    def __init__(self, walidatory):
        self.walidatory = walidatory

    def sprawdz(self, dane):
        wyniki = []

        for walidator in self.walidatory:
            poprawny, komunikat = walidator.sprawdz(dane)

            wyniki.append((
                walidator.__class__.__name__,
                poprawny,
                komunikat
            ))

        czy_poprawne = all(wynik[1] for wynik in wyniki)

        return czy_poprawne, wyniki


# Konfiguracja pipeline
pipeline = Pipeline([
    WalidatorZakresu(0, 100),
    WalidatorTypu(float),
    WalidatorBrakow()
])


# Zestawy danych testowych
zestawy = {
    "Dane poprawne": [10.0, 25.5, 50.0, 99.9],
    "Wartosc poza zakresem": [10.0, 120.0, 50.0],
    "Nieprawidlowy typ": [10.0, 20, 30.0],
    "Brak None": [10.0, None, 30.0],
    "Brak NaN": [10.0, float("nan"), 30.0],
}


print("PIPELINE Z WALIDACJA DANYCH")
print("=" * 75)

wyniki_testow = {}

for nazwa, dane in zestawy.items():
    print(f"\nTEST: {nazwa}")
    print("-" * 75)
    print(f"Dane: {dane}")

    poprawne, wyniki = pipeline.sprawdz(dane)
    wyniki_testow[nazwa] = poprawne

    for walidator, wynik, komunikat in wyniki:
        status = "OK" if wynik else "BLAD"
        print(f"{walidator}: {status} | {komunikat}")

    print(f"WYNIK KONCOWY: {'POPRAWNE' if poprawne else 'NIEPOPRAWNE'}")


# Weryfikacja
oczekiwane = {
    "Dane poprawne": True,
    "Wartosc poza zakresem": False,
    "Nieprawidlowy typ": False,
    "Brak None": False,
    "Brak NaN": False,
}

print("\nWERYFIKACJA")
print("=" * 75)

for nazwa, oczekiwany in oczekiwane.items():
    print(f"{nazwa}: {wyniki_testow[nazwa] == oczekiwany}")

print(
    "Czy wszystkie testy przeszly: "
    f"{wyniki_testow == oczekiwane}"
)
