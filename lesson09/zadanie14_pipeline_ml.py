# Lekcja 09 - Zadanie 14: Pipeline ML z roznymi transformerami

import math
import statistics


class LogTransformer:
    def przetworz(self, dane):
        if any(x < 0 for x in dane):
            raise ValueError("LogTransformer wymaga wartosci >= 0.")

        return [math.log1p(x) for x in dane]


class OutlierRemover:
    def przetworz(self, dane):
        if len(dane) < 2:
            return dane.copy()

        srednia = statistics.mean(dane)
        odchylenie = statistics.pstdev(dane)

        return [
            x for x in dane
            if abs(x - srednia) <= 3 * odchylenie
        ]


class BinningTransformer:
    def __init__(self, liczba_przedzialow=3):
        if liczba_przedzialow <= 0:
            raise ValueError("Liczba przedzialow musi byc dodatnia.")

        self.liczba_przedzialow = liczba_przedzialow

    def przetworz(self, dane):
        if not dane:
            return []

        minimum = min(dane)
        maksimum = max(dane)

        if minimum == maksimum:
            return [0 for _ in dane]

        szerokosc = (
            (maksimum - minimum) / self.liczba_przedzialow
        )

        return [
            min(
                int((x - minimum) / szerokosc),
                self.liczba_przedzialow - 1
            )
            for x in dane
        ]


class Pipeline:
    def __init__(self, kroki):
        self.kroki = kroki

    def przetworz(self, dane):
        wynik = dane.copy()

        for krok in self.kroki:
            wynik = krok.przetworz(wynik)

            print(f"\n{krok.__class__.__name__}:")
            print(wynik)

        return wynik


# Dane wejsciowe
dane = [1, 5, 10, 100, 2, 3, 8, 200, 4, 6]

# Utworzenie pipeline
pipeline = Pipeline([
    OutlierRemover(),
    LogTransformer(),
    BinningTransformer(liczba_przedzialow=3)
])

print("PIPELINE ML Z ROZNYMI TRANSFORMERAMI")
print("=" * 70)
print(f"Dane wejsciowe: {dane}")

# Uruchomienie pipeline
wynik = pipeline.przetworz(dane)

print("\nWYNIK KONCOWY")
print("=" * 70)
print(f"Przedzialy: {wynik}")

# Weryfikacja
print("\nWERYFIKACJA")
print("=" * 70)

print(f"Czy pipeline ma 3 kroki: {len(pipeline.kroki) == 3}")
print(f"Czy liczba wynikow jest poprawna: {len(wynik) == len(dane)}")
print(f"Czy wyniki sa liczbami calkowitymi: {all(isinstance(x, int) for x in wynik)}")
print(f"Czy przedzialy sa z zakresu 0-2: {all(0 <= x <= 2 for x in wynik)}")
