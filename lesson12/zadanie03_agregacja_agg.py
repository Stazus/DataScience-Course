# Lekcja 12 - Zadanie 3: Agregacja z .agg()

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# Generowanie syntetycznego datasetu
np.random.seed(42)

sales = pd.DataFrame({
    "Region": np.random.choice(["A", "B", "C"], 100),
    "Sprzedaż": np.random.randint(50, 500, 100)
})

# Kopia danych do weryfikacji
sales_original = sales.copy()

print("=" * 75)
print("AGREGACJA Z .agg() - ANALIZA SPRZEDAZY")
print("=" * 75)


# Informacje o danych
section("DANE WEJSCIOWE")

print(f"Shape: {sales.shape}")
print(f"Liczba obserwacji: {len(sales)}")
print(f"Liczba kolumn: {len(sales.columns)}")
print(f"Liczba regionow: {sales['Region'].nunique()}")
print(f"Regiony: {sorted(sales['Region'].unique())}")
print(f"Liczba NaN: {sales.isna().sum().sum()}")


# Pierwsze rekordy
section("PIERWSZE 10 REKORDOW")

print(sales.head(10).to_string(index=False))


# Statystyki calego datasetu
section("STATYSTYKI GLOBALNE SPRZEDAZY")

print(sales["Sprzedaż"].describe().round(2))


# Liczba obserwacji wedlug regionu
section("LICZBA OBSERWACJI W REGIONACH")

region_counts = sales["Region"].value_counts().sort_index()

print(region_counts)


# Glowna agregacja zgodna z wymaganiami zadania
section("AGREGACJA SPRZEDAZY WEDLUG REGIONU")

aggregation = (
    sales.groupby("Region")["Sprzedaż"]
    .agg(["min", "max", "mean", "std"])
)

print(aggregation.round(2).to_string(
    float_format=lambda x: f"{x:.2f}"
))


# Czytelne nazwy kolumn
section("TABELA AGREGACJI - POLSKIE NAZWY")

results = aggregation.rename(columns={
    "min": "Minimum",
    "max": "Maksimum",
    "mean": "Srednia",
    "std": "Odchylenie_std"
}).round(2)

print(results.to_string(
    float_format=lambda x: f"{x:.2f}"
))


# Rozszerzona agregacja
section("SZCZEGOLOWE STATYSTYKI REGIONALNE")

extended = sales.groupby("Region").agg(
    Liczba_obserwacji=("Sprzedaż", "count"),
    Suma_sprzedazy=("Sprzedaż", "sum"),
    Minimum=("Sprzedaż", "min"),
    Maksimum=("Sprzedaż", "max"),
    Srednia=("Sprzedaż", "mean"),
    Mediana=("Sprzedaż", "median"),
    Odchylenie_std=("Sprzedaż", "std")
)

# Rozstep sprzedazy
extended["Rozstep"] = (
    extended["Maksimum"] - extended["Minimum"]
)

# Wspolczynnik zmiennosci
extended["Zmiennosc_%"] = (
    extended["Odchylenie_std"]
    / extended["Srednia"] * 100
)

print(extended.round(2).to_string())


# Udzial regionow w sprzedazy
section("UDZIAL REGIONOW W CALKOWITEJ SPRZEDAZY")

total_sales = sales["Sprzedaż"].sum()

shares = pd.DataFrame({
    "Suma_sprzedazy": extended["Suma_sprzedazy"],
    "Udzial_%": (
        extended["Suma_sprzedazy"] / total_sales * 100
    )
})

print(shares.round(2))


# Ranking regionow
section("RANKING REGIONOW WEDLUG SREDNIEJ SPRZEDAZY")

ranking = results.sort_values(
    "Srednia",
    ascending=False
)

print(ranking.to_string())


# Tekstowy wykres sredniej sprzedazy
section("TEKSTOWY WYKRES SREDNIEJ SPRZEDAZY")

print("Legenda: jeden znak = okolo 10 jednostek sprzedazy")

for region, value in aggregation["mean"].items():
    bar = "█" * round(value / 10)

    print(
        f"Region {region} | "
        f"{bar:<50} {value:.2f}"
    )


# Tekstowy wykres odchylenia standardowego
section("TEKSTOWY WYKRES ODCHYLENIA STANDARDOWEGO")

print("Legenda: jeden znak = okolo 5 jednostek")

for region, value in aggregation["std"].items():
    bar = "█" * round(value / 5)

    print(
        f"Region {region} | "
        f"{bar:<40} {value:.2f}"
    )


# Tekstowy wykres udzialu w sprzedazy
section("TEKSTOWY WYKRES UDZIALU W SPRZEDAZY")

print("Legenda: jeden znak = okolo 2%")

for region, value in shares["Udzial_%"].items():
    bar = "█" * round(value / 2)

    print(
        f"Region {region} | "
        f"{bar:<50} {value:.2f}%"
    )


# Porownanie regionow
section("POROWNANIE REGIONOW")

best_region = aggregation["mean"].idxmax()
worst_region = aggregation["mean"].idxmin()

most_variable = aggregation["std"].idxmax()
least_variable = aggregation["std"].idxmin()

highest_total = extended["Suma_sprzedazy"].idxmax()

mean_difference = (
    aggregation["mean"].max()
    - aggregation["mean"].min()
)

print(
    f"Najwyzsza srednia: region {best_region} - "
    f"{aggregation.loc[best_region, 'mean']:.2f}"
)

print(
    f"Najnizsza srednia: region {worst_region} - "
    f"{aggregation.loc[worst_region, 'mean']:.2f}"
)

print(f"Roznica srednich: {mean_difference:.2f}")

print(
    f"Najwieksze odchylenie: region {most_variable} - "
    f"{aggregation.loc[most_variable, 'std']:.2f}"
)

print(
    f"Najmniejsze odchylenie: region {least_variable} - "
    f"{aggregation.loc[least_variable, 'std']:.2f}"
)

print(
    f"Najwieksza suma sprzedazy: region {highest_total} - "
    f"{extended.loc[highest_total, 'Suma_sprzedazy']}"
)


# Wnioski
section("WNIOSKI")

print("1. GroupBy dzieli dane na grupy wedlug regionu.")
print("2. Agg pozwala wykonac wiele agregacji jednoczesnie.")
print("3. Min i max okreslaja skrajne wartosci sprzedazy.")
print("4. Mean okresla srednia sprzedaz w regionie.")
print("5. Std mierzy zroznicowanie wartosci sprzedazy.")
print("6. Pandas domyslnie stosuje std z ddof=1.")
print("7. Round(2) zaokragla wyniki do dwoch miejsc.")
print(f"8. Najwyzsza srednia wystapila w regionie {best_region}.")
print(f"9. Najmniejsze odchylenie ma region {least_variable}.")
print("10. Dane sa syntetyczne, a nie rzeczywiste.")


# Podsumowanie
section("PODSUMOWANIE")

print(f"Liczba obserwacji: {len(sales)}")
print(f"Liczba regionow: {len(aggregation)}")
print(f"Liczba podstawowych agregacji: {len(aggregation.columns)}")
print(f"Calkowita sprzedaz: {total_sales}")
print(f"Globalna srednia: {sales['Sprzedaż'].mean():.2f}")
print(f"Najlepszy region wedlug sredniej: {best_region}")
print(f"Najlepszy region wedlug sumy: {highest_total}")


# Niezalezna weryfikacja agregacji za pomoca NumPy
manual_results = {}

for region in sorted(sales["Region"].unique()):
    values = sales.loc[
        sales["Region"] == region,
        "Sprzedaż"
    ].to_numpy()

    manual_results[region] = [
        np.min(values),
        np.max(values),
        np.mean(values),
        np.std(values, ddof=1)
    ]

manual_df = pd.DataFrame.from_dict(
    manual_results,
    orient="index",
    columns=["min", "max", "mean", "std"]
)


# Weryfikacja poprawnosci
section("WERYFIKACJA")

tests = {
    "Dataset ma 100 wierszy":
        len(sales) == 100,

    "Dataset ma 2 kolumny":
        len(sales.columns) == 2,

    "Istnieja 3 regiony":
        sales["Region"].nunique() == 3,

    "Regiony to A, B i C":
        set(sales["Region"]) == {"A", "B", "C"},

    "Sprzedaz miesci sie w zakresie 50-499":
        sales["Sprzedaż"].between(50, 499).all(),

    "Dataset nie zawiera NaN":
        not sales.isna().any().any(),

    "Utworzono 3 grupy":
        len(aggregation) == 3,

    "Agregacja ma shape (3, 4)":
        aggregation.shape == (3, 4),

    "Agregacja zawiera wymagane kolumny":
        list(aggregation.columns) == [
            "min", "max", "mean", "std"
        ],

    "Agregacja nie zawiera NaN":
        not aggregation.isna().any().any(),

    "Minimum nie przekracza maksimum":
        (aggregation["min"] <= aggregation["max"]).all(),

    "Srednia jest nie mniejsza od minimum":
        (aggregation["mean"] >= aggregation["min"]).all(),

    "Srednia jest nie wieksza od maksimum":
        (aggregation["mean"] <= aggregation["max"]).all(),

    "Odchylenia standardowe sa nieujemne":
        (aggregation["std"] >= 0).all(),

    "Wyniki Pandas i NumPy sa zgodne":
        np.allclose(
            aggregation.to_numpy(),
            manual_df.to_numpy()
        ),

    "Wyniki zaokraglono do 2 miejsc":
        np.allclose(
            results.to_numpy(),
            aggregation.round(2).to_numpy()
        ),

    "Uwzgledniono wszystkie obserwacje":
        extended["Liczba_obserwacji"].sum() == 100,

    "Suma sprzedazy jest zgodna":
        extended["Suma_sprzedazy"].sum() == total_sales,

    "Udzialy regionow sumuja sie do 100%":
        np.isclose(shares["Udzial_%"].sum(), 100),

    "Rozstepy sa poprawne":
        (
            extended["Rozstep"]
            == extended["Maksimum"] - extended["Minimum"]
        ).all(),

    "Ranking jest poprawnie posortowany":
        ranking["Srednia"].is_monotonic_decreasing,

    "Oryginalne dane pozostaly niezmienione":
        sales.equals(sales_original)
}

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

assert all(tests.values()), "Nie wszystkie testy zostaly zaliczone."

print("Wszystkie testy zakonczone pomyslnie.")
