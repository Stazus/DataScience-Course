# Lekcja 12 - Zadanie 2: Zliczanie obserwacji

import pandas as pd
import numpy as np


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia danych do weryfikacji
df_original = df.copy()


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


print("=" * 75)
print("ZLICZANIE OBSERWACJI - DATASET TITANIC")
print("=" * 75)


# Dane wejsciowe
section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {df.shape[1]}")
print(f"Liczba klas: {df['Pclass'].nunique()}")
print(f"Statusy przezycia: {sorted(df['Survived'].unique())}")


# Podglad danych
section("PIERWSZE 10 REKORDOW")

print(
    df[["PassengerId", "Pclass", "Survived"]]
    .head(10)
    .to_string(index=False)
)


# Grupowanie wedlug klasy i statusu przezycia
grouped = df.groupby(["Pclass", "Survived"]).size()

section("GRUPOWANIE - PCLASS I SURVIVED")

print(grouped)


# Zamiana Series na DataFrame
grouped_df = grouped.reset_index(
    name="Liczba_pasazerow"
)

section("TABELA ZLICZONYCH OBSERWACJI")

print(grouped_df.to_string(index=False))


# Utworzenie tabeli przestawnej
pivot = grouped.unstack(fill_value=0)

section("TABELA PRZESTAWNA - UNSTACK")

print(pivot)


# Alternatywna metoda - pivot_table
pivot_alternative = pd.pivot_table(
    df,
    index="Pclass",
    columns="Survived",
    values="PassengerId",
    aggfunc="count",
    fill_value=0
)

section("TABELA PRZESTAWNA - PIVOT_TABLE")

print(pivot_alternative)


# Czytelne nazwy kolumn
results = pivot.rename(
    columns={
        0: "Nie_przezyli",
        1: "Przezyli"
    }
).copy()

# Usuniecie nazwy osi kolumn
results.columns.name = None

# Liczba pasazerow w kazdej klasie
results["Razem"] = (
    results["Nie_przezyli"]
    + results["Przezyli"]
)

# Wskazniki procentowe
results["Przezywalnosc_%"] = (
    results["Przezyli"]
    / results["Razem"]
    * 100
)

results["Smiertelnosc_%"] = (
    results["Nie_przezyli"]
    / results["Razem"]
    * 100
)


section("SZCZEGOLOWE STATYSTYKI WEDLUG KLASY")

print(results.round(2))


# Globalne statystyki
total_passengers = len(df)
total_survived = int(df["Survived"].sum())
total_not_survived = total_passengers - total_survived

survival_rate = (
    total_survived / total_passengers * 100
)

mortality_rate = (
    total_not_survived / total_passengers * 100
)


# Tabela z wierszem podsumowania
summary = results.copy()

summary.loc["Razem"] = {
    "Nie_przezyli": total_not_survived,
    "Przezyli": total_survived,
    "Razem": total_passengers,
    "Przezywalnosc_%": survival_rate,
    "Smiertelnosc_%": mortality_rate
}

section("TABELA Z PODSUMOWANIEM")

print(summary.round(2))


# Rozklad liczby pasazerow wedlug klasy
section("LICZBA PASAZEROW W KAZDEJ KLASIE")

print(
    df["Pclass"]
    .value_counts()
    .sort_index()
)


# Rozklad statusu przezycia
section("ROZKLAD STATUSU PRZEZYCIA")

print(
    df["Survived"]
    .value_counts()
    .sort_index()
    .rename({
        0: "Nie przezyli",
        1: "Przezyli"
    })
)


# Tekstowy wykres liczby pasazerow
section("TEKSTOWY WYKRES LICZBY PASAZEROW")

print("Legenda: jeden znak = okolo 10 pasazerow")

for pclass, row in results.iterrows():

    count = int(row["Razem"])
    bar = "█" * round(count / 10)

    print(
        f"Klasa {pclass} | "
        f"{bar:<50} {count}"
    )


# Tekstowy wykres przezywalnosci
section("TEKSTOWY WYKRES PRZEZYWALNOSCI")

print("Legenda: jeden znak = okolo 2%")

for pclass, row in results.iterrows():

    rate = row["Przezywalnosc_%"]
    bar = "█" * round(rate / 2)

    print(
        f"Klasa {pclass} | "
        f"{bar:<50} {rate:.2f}%"
    )


# Porownanie klas
best_class = results["Przezywalnosc_%"].idxmax()
worst_class = results["Przezywalnosc_%"].idxmin()

best_rate = results.loc[
    best_class, "Przezywalnosc_%"
]

worst_rate = results.loc[
    worst_class, "Przezywalnosc_%"
]

rate_difference = best_rate - worst_rate


section("POROWNANIE KLAS")

print(
    f"Najwyzsza przezywalnosc: "
    f"klasa {best_class} - {best_rate:.2f}%"
)

print(
    f"Najnizsza przezywalnosc: "
    f"klasa {worst_class} - {worst_rate:.2f}%"
)

print(
    f"Roznica przezywalnosci: "
    f"{rate_difference:.2f} p.p."
)


# Wnioski
section("WNIOSKI")

print("1. GroupBy pozwala grupowac dane wedlug wielu kolumn.")
print("2. Size zlicza wszystkie wiersze w kazdej grupie.")
print("3. Unstack przeksztalca MultiIndex w tabele.")
print("4. Pivot_table pozwala uzyskac analogiczny wynik.")
print("5. Najwiecej pasazerow podrozowalo trzecia klasa.")
print("6. Najwyzsza przezywalnosc odnotowano w pierwszej klasie.")
print("7. Najnizsza przezywalnosc wystapila w trzeciej klasie.")
print("8. Klasa biletu wykazuje zwiazek z przezywalnoscia.")
print("9. Sama zaleznosc nie dowodzi zwiazku przyczynowego.")


# Podsumowanie
section("PODSUMOWANIE")

print(f"Liczba pasazerow: {total_passengers}")
print(f"Liczba grup: {len(grouped)}")
print(f"Liczba ocalalych: {total_survived}")
print(f"Liczba ofiar: {total_not_survived}")
print(f"Przezywalnosc: {survival_rate:.2f}%")
print(f"Smiertelnosc: {mortality_rate:.2f}%")


# Weryfikacja
section("WERYFIKACJA")

expected_counts = np.array([
    [80, 136],
    [97, 87],
    [372, 119]
])

tests = {
    "Dataset ma 891 wierszy":
        len(df) == 891,

    "Dataset ma 12 kolumn":
        df.shape[1] == 12,

    "Istnieja 3 klasy":
        df["Pclass"].nunique() == 3,

    "Istnieja 2 statusy przezycia":
        df["Survived"].nunique() == 2,

    "Utworzono 6 grup":
        len(grouped) == 6,

    "Grupowanie zwraca MultiIndex":
        isinstance(grouped.index, pd.MultiIndex),

    "Tabela grup ma 6 wierszy":
        len(grouped_df) == 6,

    "Tabela pivot ma shape (3, 2)":
        pivot.shape == (3, 2),

    "Tabela pivot nie zawiera NaN":
        not pivot.isna().any().any(),

    "Wszystkie liczebnosci sa nieujemne":
        (pivot >= 0).all().all(),

    "Liczebnosci grup sa poprawne":
        np.array_equal(
            pivot.to_numpy(),
            expected_counts
        ),

    "Unstack i pivot_table sa zgodne":
        pivot.equals(pivot_alternative),

    "Uwzgledniono wszystkich pasazerow":
        pivot.to_numpy().sum() == total_passengers,

    "Liczba ocalalych wynosi 342":
        total_survived == 342,

    "Liczba ofiar wynosi 549":
        total_not_survived == 549,

    "Liczba pasazerow w klasach jest poprawna":
        np.array_equal(
            results["Razem"].to_numpy(),
            np.array([216, 184, 491])
        ),

    "Suma pasazerow w klasach wynosi 891":
        results["Razem"].sum() == 891,

    "Suma ocalalych w klasach wynosi 342":
        results["Przezyli"].sum() == 342,

    "Suma ofiar w klasach wynosi 549":
        results["Nie_przezyli"].sum() == 549,

    "Przezywalnosc jest w zakresie 0-100":
        results["Przezywalnosc_%"].between(0, 100).all(),

    "Przezywalnosc i smiertelnosc daja 100%":
        np.allclose(
            results["Przezywalnosc_%"]
            + results["Smiertelnosc_%"],
            100
        ),

    "Najwyzsza przezywalnosc ma klasa 1":
        best_class == 1,

    "Najnizsza przezywalnosc ma klasa 3":
        worst_class == 3,

    "Globalna przezywalnosc jest poprawna":
        np.isclose(
            survival_rate,
            342 / 891 * 100
        ),

    "Oryginalne dane pozostaly niezmienione":
        df.equals(df_original)
}

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

assert all(tests.values()), "Nie wszystkie testy zostaly zaliczone."

print("Wszystkie testy zakonczone pomyslnie.")
