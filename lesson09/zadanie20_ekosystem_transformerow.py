# Lekcja 09 - Zadanie 20: Ekosystem transformerow danych


class BaseTransformer:
    def fit(self, dane):
        return self

    def transform(self, dane):
        raise NotImplementedError(
            "Klasa potomna musi implementowac metode transform()."
        )

    def fit_transform(self, dane):
        return self.fit(dane).transform(dane)


class DropNullTransformer(BaseTransformer):
    def transform(self, dane):
        return [x for x in dane if x is not None]


class ClipTransformer(BaseTransformer):
    def __init__(self, min, max):
        if min > max:
            raise ValueError("Minimum nie moze byc wieksze od maksimum.")

        self.min = min
        self.max = max

    def transform(self, dane):
        return [
            min(max(x, self.min), self.max)
            for x in dane
        ]


class SquareTransformer(BaseTransformer):
    def transform(self, dane):
        return [x ** 2 for x in dane]


class InverseTransformer(BaseTransformer):
    def transform(self, dane):
        if any(x == 0 for x in dane):
            raise ValueError(
                "Nie mozna obliczyc odwrotnosci zera."
            )

        return [1 / x for x in dane]


class Pipeline:
    def __init__(self, transformery):
        self.transformery = transformery

    def fit_transform(self, dane):
        wynik = list(dane)

        for transformer in self.transformery:
            wynik = transformer.fit_transform(wynik)

            print(
                f"{transformer.__class__.__name__}: "
                f"{wynik}"
            )

        return wynik


# Dane testowe
dane = [None, -5, 0, 2, 4, 10, 20, None]

# Pipeline z czterema transformerami
pipeline = Pipeline([
    DropNullTransformer(),
    ClipTransformer(1, 10),
    SquareTransformer(),
    InverseTransformer()
])


print("EKOSYSTEM TRANSFORMEROW DANYCH")
print("=" * 75)

print(f"\nDane wejsciowe: {dane}")

print("\nPRZETWARZANIE DANYCH")
print("=" * 75)

wynik = pipeline.fit_transform(dane)

print("\nWYNIK KONCOWY")
print("=" * 75)
print(f"Wynik: {wynik}")


# Oczekiwane wyniki poszczegolnych operacji
oczekiwane = [
    1.0,
    1.0,
    0.25,
    0.0625,
    0.01,
    0.01
]


print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy pipeline ma 4 transformery: {len(pipeline.transformery) == 4}")
print(f"Czy usunieto None: {len(wynik) == 6}")
print(f"Czy wynik jest poprawny: {wynik == oczekiwane}")
print(f"Czy wszystkie wartosci sa dodatnie: {all(x > 0 for x in wynik)}")

print(
    "Czy wszystkie klasy dziedzicza po BaseTransformer: "
    f"{all(isinstance(t, BaseTransformer) for t in pipeline.transformery)}"
)

print(
    "Czy dane wejsciowe pozostaly niezmienione: "
    f"{dane == [None, -5, 0, 2, 4, 10, 20, None]}"
)


# Test zabezpieczenia przed dzieleniem przez zero
print("\nTEST DZIELENIA PRZEZ ZERO")
print("=" * 75)

try:
    InverseTransformer().transform([1, 0, 2])
except ValueError as blad:
    print(f"Poprawnie wykryto blad: {blad}")
