# Lekcja 12 - Zadanie 4: Transform

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia danych do weryfikacji
df_original = df.copy()

print("=" * 75)
print("TRANSFORM - DATASET TITANIC")
print("=" * 75)


# Informacje o danych wejsciowych
section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {df.shape[1]}")
print(f"Liczba klas: {df['Pclass'].nunique()}")
print(f"Brakujace Fare: {df['Fare'].isna().sum()}")


# Pierwsze rekordy przed transformacja
section("PIERWSZE 10 REKORDOW PRZED TRANSFORMACJA")

print(
    df[["Pclass", "Fare"]]
    .head(10)
    .to_string(index=False)
)


# Srednia cena biletu dla kazdej klasy
section("SREDNIA CENA BILETU WEDLUG KLASY")

avg_fare = df.groupby("Pclass")["Fare"].mean()

print(avg_fare.round(2))


# Glowna operacja - transform
df["Avg_Fare_Pclass"] = (
    df.groupby("Pclass")["Fare"].transform("mean")
)


# Wynik transformacji
section("PIERWSZE 10 REKORDOW PO TRANSFORMACJI")

columns = ["Pclass", "Fare", "Avg_Fare_Pclass"]

print(
    df[columns]
    .head(10)
    .round(2)
    .to_string(index=False)
)


# Porownanie struktury danych
section("STRUKTURA DATAFRAME")

print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")

added_columns = [
    col for col in df.columns
    if col not in df_original.columns
]

print(f"Dodane kolumny: {added_columns}")
print(f"Typ nowej kolumny: {df['Avg_Fare_Pclass'].dtype}")


# Szczegolowe statystyki grupowe
section("SZCZEGOLOWE STATYSTYKI WEDLUG KLASY")

class_stats = df.groupby("Pclass").agg(
    Liczba_pasazerow=("PassengerId", "size"),
    Minimalna_cena=("Fare", "min"),
    Maksymalna_cena=("Fare", "max"),
    Srednia_cena=("Fare", "mean"),
    Mediana_ceny=("Fare", "median"),
    Odchylenie_std=("Fare", "std"),
    Wartosc_transform=("Avg_Fare_Pclass", "first")
)

print(class_stats.round(2).to_string())


# Porownanie agregacji i transformacji
section("POROWNANIE AGREGACJI I TRANSFORMACJI")

aggregation = df.groupby("Pclass")["Fare"].mean()

transformation = df.groupby("Pclass")["Fare"].transform("mean")

print(f"Liczba wynikow agregacji: {len(aggregation)}")
print(f"Liczba wynikow transformacji: {len(transformation)}")

print("\nAgregacja:")
print(aggregation.round(2))

print("\nTransformacja - pierwsze 10 wartosci:")
print(transformation.head(10).round(2).to_string())


# Unikalne wartosci transformacji w grupach
section("UNIKALNE WARTOSCI AVG_FARE_PCLASS")

unique_per_class = (
    df.groupby("Pclass")["Avg_Fare_Pclass"].nunique()
)

print(unique_per_class)

print("\nKazda klasa powinna miec jedna unikalna srednia.")


# Porownanie ceny biletu ze srednia klasy
section("POROWNANIE CENY BILETU ZE SREDNIA KLASY")

# Dodatkowa analiza na osobnej kopii
comparison = df[columns].copy()

comparison["Roznica"] = (
    comparison["Fare"] - comparison["Avg_Fare_Pclass"]
)

comparison["Roznica_%"] = (
    comparison["Roznica"]
    / comparison["Avg_Fare_Pclass"]
    * 100
)

comparison["Pozycja"] = np.select(
    [
        np.isclose(comparison["Roznica"], 0),
        comparison["Roznica"] > 0
    ],
    [
        "Rowne sredniej",
        "Powyzej sredniej"
    ],
    default="Ponizej sredniej"
)

print(
    comparison.head(10)
    .round(2)
    .to_string(index=False)
)


# Liczba pasazerow powyzej i ponizej sredniej
section("ROZKLAD CEN WZGLEDEM SREDNIEJ KLASY")

position_counts = (
    comparison.groupby(["Pclass", "Pozycja"])
    .size()
    .unstack(fill_value=0)
)

print(position_counts.to_string())


# Roznice cen pomiedzy klasami
section("POROWNANIE SREDNICH CEN KLAS")

highest_class = avg_fare.idxmax()
lowest_class = avg_fare.idxmin()

highest_fare = avg_fare.max()
lowest_fare = avg_fare.min()

fare_difference = highest_fare - lowest_fare
fare_ratio = highest_fare / lowest_fare

print(
    f"Najwyzsza srednia: klasa {highest_class}"
    f" - {highest_fare:.2f}"
)

print(
    f"Najnizsza srednia: klasa {lowest_class}"
    f" - {lowest_fare:.2f}"
)

print(f"Roznica srednich: {fare_difference:.2f}")
print(f"Stosunek srednich cen: {fare_ratio:.2f}x")


# Tekstowy wykres srednich cen
section("TEKSTOWY WYKRES SREDNIEJ CENY BILETU")

print("Legenda: jeden znak = okolo 2 jednostek ceny")

for pclass, fare in avg_fare.items():
    bar = "█" * int(round(fare / 2))

    print(
        f"Klasa {pclass} | "
        f"{bar:<45} {fare:.2f}"
    )


# Srednia globalna i srednia wazona
section("SREDNIA GLOBALNA I SREDNIA WAZONA")

global_mean = df["Fare"].mean()

weighted_mean = np.average(
    class_stats["Srednia_cena"],
    weights=class_stats["Liczba_pasazerow"]
)

transform_mean = df["Avg_Fare_Pclass"].mean()

print(f"Srednia globalna Fare: {global_mean:.4f}")
print(f"Srednia wazona klas: {weighted_mean:.4f}")
print(f"Srednia kolumny transform: {transform_mean:.4f}")


# Porownanie zuzycia pamieci
section("ZUZYCIE PAMIECI")

memory_before = (
    df_original.memory_usage(deep=True).sum()
)

memory_after = (
    df.memory_usage(deep=True).sum()
)

memory_increase = memory_after - memory_before

print(f"Przed: {memory_before / 1024:.2f} KiB")
print(f"Po: {memory_after / 1024:.2f} KiB")
print(f"Wzrost: {memory_increase / 1024:.2f} KiB")


# Wnioski
section("WNIOSKI")

conclusions = [
    "GroupBy grupuje pasazerow wedlug klasy.",
    "Transform oblicza srednia osobno dla kazdej grupy.",
    "Transform zachowuje liczbe wierszy i indeksy.",
    "Kazdy pasazer otrzymuje srednia ceny swojej klasy.",
    "Agg i mean redukuja dane do poziomu grup.",
    "Transform pozwala dodawac nowe cechy do DataFrame.",
    "Najwyzsza srednia cena wystepuje w pierwszej klasie.",
    "Nowa kolumna pozwala porownac cene ze srednia klasy.",
    "Nie zmieniono wartosci istniejacych kolumn.",
    "W projektach ML statystyki grupowe nalezy wyznaczac na danych treningowych."
]

for number, conclusion in enumerate(conclusions, 1):
    print(f"{number}. {conclusion}")


# Podsumowanie
section("PODSUMOWANIE")

print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba klas: {df['Pclass'].nunique()}")
print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")
print("Nowa kolumna: Avg_Fare_Pclass")
print(f"Brakujace wartosci: {df['Avg_Fare_Pclass'].isna().sum()}")

for pclass, fare in avg_fare.items():
    print(f"Srednia klasy {pclass}: {fare:.2f}")


# Niezalezna metoda weryfikacji
expected_values = df["Pclass"].map(avg_fare)

expected_means = np.array([
    df.loc[df["Pclass"] == pclass, "Fare"].mean()
    for pclass in avg_fare.index
])


# Testy poprawnosci
section("WERYFIKACJA")

tests = {
    "Dataset ma 891 wierszy":
        len(df_original) == 891,

    "Dataset ma poczatkowo 12 kolumn":
        df_original.shape[1] == 12,

    "Istnieja 3 klasy":
        df["Pclass"].nunique() == 3,

    "Dodano kolumne Avg_Fare_Pclass":
        "Avg_Fare_Pclass" in df.columns,

    "Dodano tylko jedna kolumne":
        added_columns == ["Avg_Fare_Pclass"],

    "Wynik ma shape (891, 13)":
        df.shape == (891, 13),

    "Zachowano wszystkie wiersze":
        len(df) == len(df_original),

    "Zachowano oryginalne indeksy":
        df.index.equals(df_original.index),

    "Transform zwraca 891 wartosci":
        len(transformation) == 891,

    "Agregacja zwraca 3 wartosci":
        len(aggregation) == 3,

    "Nowa kolumna ma typ numeryczny":
        pd.api.types.is_numeric_dtype(
            df["Avg_Fare_Pclass"]
        ),

    "Nowa kolumna nie zawiera NaN":
        df["Avg_Fare_Pclass"].notna().all(),

    "Kazda klasa ma jedna unikalna srednia":
        unique_per_class.eq(1).all(),

    "Transform i map zwracaja zgodne wyniki":
        np.allclose(
            df["Avg_Fare_Pclass"],
            expected_values
        ),

    "Srednie klas obliczono poprawnie":
        np.allclose(
            avg_fare.to_numpy(),
            expected_means
        ),

    "Agregacja i transform sa zgodne":
        np.allclose(
            class_stats["Srednia_cena"],
            class_stats["Wartosc_transform"]
        ),

    "Srednie ceny sa dodatnie":
        df["Avg_Fare_Pclass"].gt(0).all(),

    "Pierwsza klasa ma najwyzsza srednia":
        highest_class == 1,

    "Trzecia klasa ma najnizsza srednia":
        lowest_class == 3,

    "Srednia wazona jest poprawna":
        np.isclose(global_mean, weighted_mean),

    "Srednia transform jest zgodna z globalna":
        np.isclose(global_mean, transform_mean),

    "Roznice cen obliczono poprawnie":
        np.allclose(
            comparison["Roznica"],
            df["Fare"] - df["Avg_Fare_Pclass"]
        ),

    "Uwzgledniono wszystkich pasazerow":
        position_counts.to_numpy().sum() == len(df),

    "Zwiekszono pamiec po dodaniu kolumny":
        memory_after > memory_before,

    "Istniejace kolumny pozostaly niezmienione":
        df[df_original.columns].equals(df_original)
}

for description, result in tests.items():
    print(f"Czy {description}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

if all(tests.values()):
    print("Wszystkie testy zakonczone pomyslnie.")
else:
    raise AssertionError("Nie wszystkie testy zostaly zaliczone.")
