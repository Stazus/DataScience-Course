# Lekcja 12 - Zadanie 16: Target Encoding z walidacja

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


def target_encoding_oof(
    data,
    category,
    target,
    folds
):
    """Oblicza Out-of-Fold Target Encoding."""

    encoded = pd.Series(
        np.nan,
        index=data.index,
        dtype=float
    )

    fold_details = []

    for i, validation_idx in enumerate(folds):

        # Pozostale cztery foldy
        train_idx = np.concatenate([
            fold
            for j, fold in enumerate(folds)
            if j != i
        ])

        train = data.iloc[train_idx]
        validation = data.iloc[validation_idx]

        # Srednie targetu tylko na foldach treningowych
        mapping = train.groupby(category)[target].mean()

        # Wartosc awaryjna dla nieznanych kategorii
        global_mean = train[target].mean()

        # Kodowanie foldu walidacyjnego
        values = (
            validation[category]
            .map(mapping)
            .fillna(global_mean)
        )

        encoded.iloc[validation_idx] = values.to_numpy()

        fold_details.append({
            "Fold": i + 1,
            "Train": len(train),
            "Validation": len(validation),
            "Global_mean": global_mean,
            "Mapping": mapping.to_dict(),
            "Overlap": len(
                np.intersect1d(train_idx, validation_idx)
            )
        })

    return encoded, fold_details


def histogram_text(series, bins):
    """Tworzy tekstowy histogram rozkladu."""

    counts, edges = np.histogram(
        series.dropna(),
        bins=bins
    )

    max_count = counts.max()

    for i, count in enumerate(counts):

        length = (
            int(round(count / max_count * 40))
            if max_count > 0
            else 0
        )

        bar = "█" * length

        print(
            f"{edges[i]:.2f} - {edges[i + 1]:.2f}"
            f" | {bar:<40} {count:>5}"
        )


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia oryginalnych danych
df_original = df.copy()

print("=" * 75)
print("TARGET ENCODING Z WALIDACJA - TITANIC")
print("=" * 75)


section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")

print(
    f"Brakujace Embarked: "
    f"{df['Embarked'].isna().sum()}"
)

print(
    f"Brakujace Survived: "
    f"{df['Survived'].isna().sum()}"
)

print(
    f"Globalna przezywalnosc: "
    f"{df['Survived'].mean():.4f}"
)


section("PIERWSZE 10 REKORDOW")

print(
    df[
        ["PassengerId", "Embarked", "Survived"]
    ].head(10).to_string(index=False)
)


section("ROZKLAD KATEGORII EMBARKED")

print(
    df["Embarked"]
    .value_counts(dropna=False)
    .to_string()
)


# Kopia robocza do kodowania
# Brakujace kategorie otrzymuja osobna etykiete
work = df[["Embarked", "Survived"]].copy()

work["Embarked"] = (
    work["Embarked"].fillna("Unknown")
)


section("STATYSTYKI WEDLUG PORTU")

port_stats = work.groupby("Embarked").agg(
    Liczba_pasazerow=("Survived", "size"),
    Przezyli=("Survived", "sum"),
    Survival_rate=("Survived", "mean")
)

port_stats["Survival_rate_%"] = (
    port_stats["Survival_rate"] * 100
)

print(port_stats.round(4).to_string())


section("NAIWNY TARGET ENCODING")

# UWAGA:
# Ta metoda wykorzystuje target calego datasetu.
# Sluzy tylko do porownania, nie do treningu modelu.

naive_mapping = (
    work.groupby("Embarked")["Survived"]
    .mean()
)

df["Embarked_Target_Naive"] = (
    work["Embarked"].map(naive_mapping)
)

print(naive_mapping.round(6).to_string())

print(
    "\nNaiwny encoding wykorzystuje rowniez "
    "target kodowanego pasazera."
)

print(
    "Powoduje to ryzyko wycieku danych "
    "(data leakage)."
)


section("LOSOWY PODZIAL NA 5 FOLDOW")

np.random.seed(42)

indices = np.random.permutation(len(df))

folds = np.array_split(indices, 5)

for i, fold in enumerate(folds, start=1):

    print(
        f"Fold {i}: {len(fold)} obserwacji"
    )

print(
    f"\nSuma obserwacji: "
    f"{sum(len(fold) for fold in folds)}"
)


# Przypisanie numeru foldu do kazdego pasazera
fold_ids = np.zeros(len(df), dtype=int)

for i, fold in enumerate(folds, start=1):
    fold_ids[fold] = i

df["Fold"] = fold_ids


section("OUT-OF-FOLD TARGET ENCODING")

df["Embarked_Target"], fold_details = (
    target_encoding_oof(
        data=work,
        category="Embarked",
        target="Survived",
        folds=folds
    )
)

for detail in fold_details:

    print(f"\nFOLD {detail['Fold']}")
    print("-" * 50)

    print(f"Train: {detail['Train']}")
    print(f"Validation: {detail['Validation']}")

    print(
        f"Wspolne indeksy: {detail['Overlap']}"
    )

    print(
        f"Globalna srednia train: "
        f"{detail['Global_mean']:.6f}"
    )

    print("Mapowanie kategorii:")

    for category, value in sorted(
        detail["Mapping"].items()
    ):
        print(f"  {category}: {value:.6f}")


section("PODSUMOWANIE FOLDOW")

fold_summary = pd.DataFrame([
    {
        "Fold": detail["Fold"],
        "Train": detail["Train"],
        "Validation": detail["Validation"],
        "Global_mean": detail["Global_mean"],
        "Overlap": detail["Overlap"]
    }
    for detail in fold_details
])

print(
    fold_summary.round(6)
    .to_string(index=False)
)


section("MAPOWANIE KATEGORII W FOLDACH")

mapping_table = pd.DataFrame(
    [
        detail["Mapping"]
        for detail in fold_details
    ],
    index=[
        f"Fold_{detail['Fold']}"
        for detail in fold_details
    ]
)

print(mapping_table.round(6).to_string())

print(
    "\nNaN oznacza kategorie nieobecna "
    "w czesci treningowej danego foldu."
)


section("PIERWSZE 20 REKORDOW PO ENCODINGU")

columns = [
    "PassengerId",
    "Embarked",
    "Survived",
    "Fold",
    "Embarked_Target_Naive",
    "Embarked_Target"
]

print(
    df[columns].head(20)
    .round(6)
    .to_string(index=False)
)


section("STRUKTURA DATAFRAME")

print(f"Shape przed: {df_original.shape}")
print(f"Shape po: {df.shape}")

print(
    "Dodane kolumny:",
    df.columns.difference(
        df_original.columns
    ).tolist()
)

print(
    f"Typ Embarked_Target: "
    f"{df['Embarked_Target'].dtype}"
)

print(
    f"Brakujace wartosci OOF: "
    f"{df['Embarked_Target'].isna().sum()}"
)


section("POROWNANIE ROZKLADOW - DESCRIBE")

comparison = df[
    [
        "Embarked_Target_Naive",
        "Embarked_Target"
    ]
].describe()

print(comparison.round(6).to_string())


section("POROWNANIE WEDLUG KATEGORII")

category_comparison = df.groupby(
    "Embarked",
    dropna=False
).agg(
    Liczba=("Survived", "size"),
    Naive_mean=("Embarked_Target_Naive", "mean"),
    OOF_mean=("Embarked_Target", "mean"),
    OOF_std=("Embarked_Target", "std"),
    OOF_min=("Embarked_Target", "min"),
    OOF_max=("Embarked_Target", "max"),
    OOF_unique=("Embarked_Target", "nunique")
)

print(
    category_comparison.round(6).to_string()
)


section("POROWNANIE WEDLUG FOLDOW")

fold_comparison = df.groupby("Fold").agg(
    Liczba=("Survived", "size"),
    Survival_rate=("Survived", "mean"),
    Naive_mean=("Embarked_Target_Naive", "mean"),
    OOF_mean=("Embarked_Target", "mean"),
    OOF_std=("Embarked_Target", "std")
)

print(fold_comparison.round(6).to_string())


section("MACIERZ KORELACJI")

correlation_matrix = df[
    [
        "Embarked_Target_Naive",
        "Embarked_Target",
        "Survived"
    ]
].corr()

print(
    correlation_matrix.round(6).to_string()
)

correlation = df[
    "Embarked_Target_Naive"
].corr(df["Embarked_Target"])

print(
    f"\nKorelacja Naive vs OOF: "
    f"{correlation:.6f}"
)

print(
    "Korelacja nie jest samodzielnym dowodem "
    "braku wycieku danych."
)


section("ANALIZA ROZNIC MIEDZY METODAMI")

difference = (
    df["Embarked_Target"]
    - df["Embarked_Target_Naive"]
)

absolute_difference = difference.abs()

mae = absolute_difference.mean()

rmse = np.sqrt(
    np.mean(difference ** 2)
)

print(
    f"Srednia roznica: "
    f"{difference.mean():.6f}"
)

print(f"MAE: {mae:.6f}")
print(f"RMSE: {rmse:.6f}")

print(
    f"Maksymalna roznica bezwzgledna: "
    f"{absolute_difference.max():.6f}"
)

print(
    f"Liczba roznych wartosci: "
    f"{(~np.isclose(difference, 0)).sum()}"
)

print(
    f"Unikalne wartosci Naive: "
    f"{df['Embarked_Target_Naive'].nunique()}"
)

print(
    f"Unikalne wartosci OOF: "
    f"{df['Embarked_Target'].nunique()}"
)


section("NAJWIEKSZE ROZNICE - TOP 10")

difference_table = df[columns].copy()

difference_table["Roznica"] = difference

difference_table["Roznica_abs"] = (
    absolute_difference
)

print(
    difference_table
    .sort_values(
        "Roznica_abs",
        ascending=False
    )
    .head(10)
    .round(6)
    .to_string(index=False)
)


section("TEKSTOWY HISTOGRAM - NAIVE")

bins = np.linspace(0, 1, 21)

histogram_text(
    df["Embarked_Target_Naive"],
    bins
)


section("TEKSTOWY HISTOGRAM - OUT-OF-FOLD")

histogram_text(
    df["Embarked_Target"],
    bins
)


section("SREDNI ENCODING WEDLUG PORTU")

print(
    "Legenda: jeden znak = okolo 2%"
)

for category, row in category_comparison.iterrows():

    label = (
        "Unknown"
        if pd.isna(category)
        else str(category)
    )

    naive_value = row["Naive_mean"]
    oof_value = row["OOF_mean"]

    naive_bar = "█" * int(
        round(naive_value * 50)
    )

    oof_bar = "█" * int(
        round(oof_value * 50)
    )

    print(f"\nPort: {label}")

    print(
        f"Naive | {naive_bar:<50}"
        f" {naive_value * 100:.2f}%"
    )

    print(
        f"OOF   | {oof_bar:<50}"
        f" {oof_value * 100:.2f}%"
    )


section("OBSLUGA BRAKUJACYCH KATEGORII")

missing_mask = df["Embarked"].isna()

print(
    f"Liczba brakujacych Embarked: "
    f"{missing_mask.sum()}"
)

print(
    df.loc[missing_mask, columns]
    .round(6)
    .to_string(index=False)
)

print(
    "\nBraki potraktowano jako kategorie Unknown."
)

print(
    "Jesli kategoria nie wystepuje w train, "
    "stosowana jest srednia targetu z train."
)


section("TEST DATA LEAKAGE - ZMIANA TARGETU")

# Zmieniamy target wszystkich pasazerow
# z pierwszego foldu walidacyjnego.
#
# Ich wartosci OOF nie powinny sie zmienic,
# poniewaz nie uczestnicza w obliczaniu
# wlasnego mapowania.

modified_work = work.copy()

validation_idx = folds[0]

target_col = modified_work.columns.get_loc(
    "Survived"
)

modified_work.iloc[
    validation_idx,
    target_col
] = (
    1 - modified_work.iloc[
        validation_idx,
        target_col
    ]
)

modified_oof, _ = target_encoding_oof(
    data=modified_work,
    category="Embarked",
    target="Survived",
    folds=folds
)

original_values = (
    df["Embarked_Target"]
    .iloc[validation_idx]
    .to_numpy()
)

modified_values = (
    modified_oof
    .iloc[validation_idx]
    .to_numpy()
)

leakage_test = np.allclose(
    original_values,
    modified_values
)

print(
    f"Zmienione targety: "
    f"{len(validation_idx)}"
)

print(
    f"Maksymalna zmiana OOF w foldzie 1: "
    f"{np.abs(original_values - modified_values).max():.10f}"
)

print(
    f"Czy encoding foldu 1 pozostal niezmieniony: "
    f"{leakage_test}"
)


section("TEST DATA LEAKAGE - WSZYSTKIE FOLDY")

leakage_results = []

for i, validation_idx in enumerate(folds):

    modified_work = work.copy()

    modified_work.iloc[
        validation_idx,
        target_col
    ] = (
        1 - modified_work.iloc[
            validation_idx,
            target_col
        ]
    )

    modified_encoding, _ = target_encoding_oof(
        modified_work,
        "Embarked",
        "Survived",
        folds
    )

    unchanged = np.allclose(
        df["Embarked_Target"]
        .iloc[validation_idx],
        modified_encoding.iloc[validation_idx]
    )

    leakage_results.append(unchanged)

    print(
        f"Fold {i + 1}: "
        f"brak wplywu wlasnego targetu = {unchanged}"
    )


section("TEST NIEZALEZNY - RECZNE OBLICZENIA")

manual_results = []

for i, validation_idx in enumerate(folds):

    train_idx = np.setdiff1d(
        np.arange(len(df)),
        validation_idx
    )

    train = work.iloc[train_idx]

    manual_values = []

    for position in validation_idx:

        category = work.iloc[position]["Embarked"]

        group = train.loc[
            train["Embarked"] == category,
            "Survived"
        ]

        if len(group) > 0:
            value = group.mean()
        else:
            value = train["Survived"].mean()

        manual_values.append(value)

    correct = np.allclose(
        df["Embarked_Target"]
        .iloc[validation_idx],
        manual_values
    )

    manual_results.append(correct)

    print(
        f"Fold {i + 1}: "
        f"zgodnosc z recznymi obliczeniami = {correct}"
    )


section("TEST NIEZNANEJ KATEGORII")

# Syntetyczny przyklad sprawdzajacy fallback
test_data = pd.DataFrame({
    "Embarked": ["A", "A", "B", "C"],
    "Survived": [0, 1, 1, 0]
})

test_folds = [
    np.array([0, 1]),
    np.array([2, 3])
]

test_encoding, _ = target_encoding_oof(
    test_data,
    "Embarked",
    "Survived",
    test_folds
)

fallback_correct = np.allclose(
    test_encoding,
    [0.5, 0.5, 0.5, 0.5]
)

print(
    f"Uzyskane wartosci: "
    f"{test_encoding.tolist()}"
)

print(
    f"Czy fallback dziala poprawnie: "
    f"{fallback_correct}"
)


section("TEST POWTARZALNOSCI")

np.random.seed(42)

repeat_indices = np.random.permutation(
    len(df)
)

repeat_folds = np.array_split(
    repeat_indices,
    5
)

repeat_encoding, _ = target_encoding_oof(
    work,
    "Embarked",
    "Survived",
    repeat_folds
)

reproducible = np.allclose(
    df["Embarked_Target"],
    repeat_encoding
)

print(
    f"Czy wyniki sa powtarzalne: "
    f"{reproducible}"
)


section("ZUZYCIE PAMIECI")

memory_before = (
    df_original.memory_usage(deep=True).sum()
    / 1024
)

memory_after = (
    df.memory_usage(deep=True).sum()
    / 1024
)

print(f"Przed: {memory_before:.2f} KiB")
print(f"Po: {memory_after:.2f} KiB")

print(
    f"Wzrost: "
    f"{memory_after - memory_before:.2f} KiB"
)


section("DATAFRAME Z DOCELOWA CECHA")

# Usuwamy kolumny diagnostyczne.
# Naiwny encoding nie powinien byc cecha ML.

df_final = df.drop(
    columns=[
        "Embarked_Target_Naive",
        "Fold"
    ]
)

print(f"Shape koncowy: {df_final.shape}")

print(
    df_final[
        [
            "PassengerId",
            "Embarked",
            "Embarked_Target"
        ]
    ].head(10).round(6).to_string(index=False)
)


section("WNIOSKI")

conclusions = [
    "Target Encoding zamienia kategorie na liczby.",
    "Naiwny encoding wykorzystuje caly target.",
    "Naiwny encoding moze powodowac data leakage.",
    "OOF dzieli dane na rozlaczne foldy.",
    "Kazdy fold jest kodowany na pozostalych foldach.",
    "Target kodowanego foldu nie uczestniczy w mapowaniu.",
    "OOF zachowuje liczbe wierszy i indeksy.",
    "Nieznane kategorie wymagaja wartosci awaryjnej.",
    "Fallback wykorzystuje srednia z czesci treningowej.",
    "Seed zapewnia powtarzalnosc podzialu.",
    "Korelacja nie dowodzi braku data leakage.",
    "Rzadkie kategorie moga miec niestabilne srednie.",
    "W praktyce mozna stosowac smoothing.",
    "Dane testowe kodujemy mapowaniem z train.",
    "Podzial train/test wykonujemy przed encodingiem.",
    "Naiwnego encodingu nie uzywamy jako cechy ML.",
    "OOF jest przykladem supervised feature engineering.",
    "W zadaniu wykorzystano tylko Pandas i NumPy."
]

for i, conclusion in enumerate(
    conclusions,
    start=1
):
    print(f"{i}. {conclusion}")


section("PODSUMOWANIE")

print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba foldow: {len(folds)}")
print("Seed: 42")

print(
    f"Liczebnosci foldow: "
    f"{[len(fold) for fold in folds]}"
)

print("Kodowana zmienna: Embarked")
print("Target: Survived")
print("Nowa cecha: Embarked_Target")

print(
    f"Korelacja Naive vs OOF: "
    f"{correlation:.6f}"
)

print(f"MAE: {mae:.6f}")
print(f"RMSE: {rmse:.6f}")

print(
    f"Brakujace wartosci OOF: "
    f"{df['Embarked_Target'].isna().sum()}"
)

print(
    f"Testy data leakage: "
    f"{sum(leakage_results)}/5"
)

print(f"Shape koncowy: {df_final.shape}")


section("WERYFIKACJA")

all_indices = np.concatenate(folds)

fold_sizes = [
    len(fold)
    for fold in folds
]

tests = {
    "Dataset ma 891 wierszy":
        len(df) == 891,

    "Dataset ma poczatkowo 12 kolumn":
        df_original.shape[1] == 12,

    "Target jest binarny":
        set(work["Survived"].unique()) == {0, 1},

    "Target nie zawiera NaN":
        work["Survived"].notna().all(),

    "Istnieja 3 oryginalne porty":
        df_original["Embarked"].nunique() == 3,

    "Istnieja 4 kategorie robocze":
        work["Embarked"].nunique() == 4,

    "Braki kategorii zostaly obsluzone":
        work["Embarked"].notna().all(),

    "Utworzono 5 foldow":
        len(folds) == 5,

    "Foldy zawieraja 891 indeksow":
        len(all_indices) == 891,

    "Indeksy foldow sa unikalne":
        len(np.unique(all_indices)) == len(df),

    "Foldy pokrywaja caly dataset":
        np.array_equal(
            np.sort(all_indices),
            np.arange(len(df))
        ),

    "Foldy sa zrownowazone":
        max(fold_sizes) - min(fold_sizes) <= 1,

    "Liczebnosci foldow sa poprawne":
        fold_sizes == [179, 178, 178, 178, 178],

    "Train i validation sa rozlaczne":
        all(
            detail["Overlap"] == 0
            for detail in fold_details
        ),

    "Train i validation obejmuja caly dataset":
        all(
            detail["Train"]
            + detail["Validation"] == len(df)
            for detail in fold_details
        ),

    "Kazdy fold ma czesc treningowa":
        all(
            detail["Train"] > 0
            for detail in fold_details
        ),

    "Dodano Embarked_Target":
        "Embarked_Target" in df.columns,

    "Dodano naiwny encoding":
        "Embarked_Target_Naive" in df.columns,

    "Dodano numery foldow":
        "Fold" in df.columns,

    "Numery foldow sa poprawne":
        set(df["Fold"].unique()) == {1, 2, 3, 4, 5},

    "OOF ma 891 wartosci":
        len(df["Embarked_Target"]) == 891,

    "Naive ma 891 wartosci":
        len(df["Embarked_Target_Naive"]) == 891,

    "OOF nie zawiera NaN":
        df["Embarked_Target"].notna().all(),

    "Naive nie zawiera NaN":
        df["Embarked_Target_Naive"].notna().all(),

    "OOF ma typ numeryczny":
        pd.api.types.is_numeric_dtype(
            df["Embarked_Target"]
        ),

    "Naive ma typ numeryczny":
        pd.api.types.is_numeric_dtype(
            df["Embarked_Target_Naive"]
        ),

    "OOF miesci sie w zakresie 0-1":
        df["Embarked_Target"].between(0, 1).all(),

    "Naive miesci sie w zakresie 0-1":
        df["Embarked_Target_Naive"]
        .between(0, 1).all(),

    "OOF zawiera skonczone wartosci":
        np.isfinite(df["Embarked_Target"]).all(),

    "Naive zawiera skonczone wartosci":
        np.isfinite(
            df["Embarked_Target_Naive"]
        ).all(),

    "Naive ma jedna wartosc na kategorie":
        df.groupby(
            "Embarked",
            dropna=False
        )["Embarked_Target_Naive"]
        .nunique().eq(1).all(),

    "OOF ma wiecej unikalnych wartosci":
        df["Embarked_Target"].nunique()
        > df["Embarked_Target_Naive"].nunique(),

    "Naive i OOF nie sa identyczne":
        not np.allclose(
            df["Embarked_Target"],
            df["Embarked_Target_Naive"]
        ),

    "Korelacja jest skonczona":
        np.isfinite(correlation),

    "Korelacja miesci sie w zakresie -1 do 1":
        -1 <= correlation <= 1,

    "Korelacja Pandas i NumPy jest zgodna":
        np.isclose(
            correlation,
            np.corrcoef(
                df["Embarked_Target_Naive"],
                df["Embarked_Target"]
            )[0, 1]
        ),

    "Macierz korelacji ma shape 3x3":
        correlation_matrix.shape == (3, 3),

    "Macierz korelacji jest symetryczna":
        np.allclose(
            correlation_matrix,
            correlation_matrix.T
        ),

    "MAE jest nieujemne":
        mae >= 0,

    "RMSE jest nieujemne":
        rmse >= 0,

    "RMSE nie jest mniejsze od MAE":
        rmse + 1e-12 >= mae,

    "Histogram Naive obejmuje wszystkie dane":
        np.histogram(
            df["Embarked_Target_Naive"],
            bins=bins
        )[0].sum() == len(df),

    "Histogram OOF obejmuje wszystkie dane":
        np.histogram(
            df["Embarked_Target"],
            bins=bins
        )[0].sum() == len(df),

    "Test data leakage dla foldu 1":
        leakage_test,

    "Test data leakage dla wszystkich foldow":
        all(leakage_results),

    "Reczne obliczenia sa zgodne":
        all(manual_results),

    "Fallback dla nieznanej kategorii dziala":
        fallback_correct,

    "Wyniki sa powtarzalne":
        reproducible,

    "Zachowano oryginalne indeksy":
        df.index.equals(df_original.index),

    "Zachowano wszystkie oryginalne kolumny":
        df[df_original.columns].equals(
            df_original
        ),

    "Koncowy DataFrame ma 13 kolumn":
        df_final.shape == (891, 13),

    "Koncowy DataFrame zawiera OOF":
        "Embarked_Target" in df_final.columns,

    "Usunieto naiwny encoding z wyniku":
        "Embarked_Target_Naive"
        not in df_final.columns,

    "Usunieto diagnostyczna kolumne Fold":
        "Fold" not in df_final.columns,

    "Koncowa cecha nie zawiera NaN":
        df_final["Embarked_Target"].notna().all(),

    "Koncowa cecha miesci sie w zakresie 0-1":
        df_final["Embarked_Target"]
        .between(0, 1).all(),

    "Suma liczebnosci kategorii jest poprawna":
        category_comparison["Liczba"].sum()
        == len(df),

    "Suma liczebnosci foldow jest poprawna":
        fold_comparison["Liczba"].sum()
        == len(df),

    "Globalna przezywalnosc jest poprawna":
        np.isclose(
            df["Survived"].mean(),
            342 / 891
        ),

    "Oryginalny target pozostal niezmieniony":
        df_final["Survived"].equals(
            df_original["Survived"]
        )
}

passed = 0

for name, result in tests.items():

    result = bool(result)

    print(f"Czy {name}: {result}")

    if result:
        passed += 1

print(
    f"\nZaliczone testy: "
    f"{passed}/{len(tests)}"
)

if passed == len(tests):
    print(
        "Wszystkie testy zakonczone pomyslnie."
    )
else:
    raise AssertionError(
        "Nie wszystkie testy zostaly zaliczone."
    )
