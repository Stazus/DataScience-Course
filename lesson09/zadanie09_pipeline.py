# Lekcja 09 - Zadanie 9: Pipeline z wieloma krokami


# Komponent 1 - filtrowanie liczb ujemnych
class FiltrowanieDodatnich:
    def przetworz(self, dane):
        return [liczba for liczba in dane if liczba >= 0]


# Komponent 2 - zaokraglanie do liczb calkowitych
class Zaokraglanie:
    def przetworz(self, dane):
        return [round(liczba) for liczba in dane]


# Komponent 3 - skalowanie danych
class Skalowanie:
    def __init__(self, wspolczynnik):
        self.wspolczynnik = wspolczynnik

    def przetworz(self, dane):
        return [
            liczba * self.wspolczynnik
            for liczba in dane
        ]


# Komponent 4 - sumowanie danych
class Sumowanie:
    def przetworz(self, dane):
        return sum(dane)


# Klasa laczaca wszystkie komponenty
class Pipeline:
    def __init__(self, kroki):
        self.kroki = kroki

    def uruchom(self, dane):
        wynik = dane

        for numer, krok in enumerate(self.kroki, start=1):
            wynik = krok.przetworz(wynik)
            print(
                f"Krok {numer} - "
                f"{type(krok).__name__}: {wynik}"
            )

        return wynik


# Dane wejsciowe
dane = [1.7, -3.2, 5.8, -1.1, 8.3, 2.4]

# Utworzenie pipeline
pipeline = Pipeline([
    FiltrowanieDodatnich(),
    Zaokraglanie(),
    Skalowanie(2),
    Sumowanie()
])


print("PIPELINE Z WIELOMA KROKAMI")
print("=" * 65)
print(f"Dane wejsciowe: {dane}")

print("\nPRZETWARZANIE")
print("=" * 65)

wynik = pipeline.uruchom(dane)


print("\nWYNIK KONCOWY")
print("=" * 65)
print(f"Suma po przetworzeniu: {wynik}")


# Weryfikacja
oczekiwany_wynik = 36

print("\nWERYFIKACJA")
print("=" * 65)
print(f"Czy wynik jest poprawny: {wynik == oczekiwany_wynik}")
print(f"Czy pipeline ma 4 kroki: {len(pipeline.kroki) == 4}")
print(f"Czy wynik jest liczba: {isinstance(wynik, (int, float))}")
