# Lekcja 11 - Zadanie 20: Efektywnosc pamieciowa - benchmark

import pandas as pd
import numpy as np


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Konfiguracja benchmarku
selected_columns = [
    "Name", "Age", "Sex", "Pclass", "Survived"
]

int8_columns = [
    "Pclass", "Survived", "SibSp", "Parch"
]

category_columns = ["Sex", "Embarked"]

chunk_size = 100

# Dydaktyczny wspolczynnik zuzycia energii
energy_factor = 0.0003

# Funkcja obliczajaca pamiec DataFrame w KiB
def memory_kb(df: pd.DataFrame) -> float:
    return df.memory_usage(deep=True).sum() / 1024


print("EFEKTYWNOSC PAMIECIOWA - BENCHMARK TITANIC")
print("=" * 75)

# ==========================================================
# WARIANT 1 - PELNE WCZYTANIE
# ==========================================================

df_full = pd.read_csv(url)

df_original = df_full.copy()

memory_full = memory_kb(df_full)

print("\nWARIANT 1 - PELNE WCZYTANIE")
print("=" * 75)

print(f"Shape: {df_full.shape}")
print(f"Liczba wierszy: {len(df_full)}")
print(f"Liczba kolumn: {len(df_full.columns)}")
print(f"Pamiec: {memory_full:.2f} KiB")

# ==========================================================
# WARIANT 2 - WYBRANE KOLUMNY
# ==========================================================

df_selected = pd.read_csv(
    url,
    usecols=selected_columns
)

memory_selected = memory_kb(df_selected)

print("\nWARIANT 2 - USECOLS")
print("=" * 75)

print(f"Shape: {df_selected.shape}")
print(f"Kolumny: {df_selected.columns.tolist()}")
print(f"Pamiec: {memory_selected:.2f} KiB")

# ==========================================================
# WARIANT 3 - BATCH PROCESSING
# ==========================================================

batch_memories = []
batch_rows = []

print("\nWARIANT 3 - CHUNKSIZE=100")
print("=" * 75)

print(f"{'Batch':>5} {'Wiersze':>8} {'Pamiec KiB':>15}")

with pd.read_csv(url, chunksize=chunk_size) as reader:

    for batch_number, chunk in enumerate(reader, start=1):

        chunk_memory = memory_kb(chunk)

        batch_memories.append(chunk_memory)
        batch_rows.append(len(chunk))

        print(
            f"{batch_number:>5} "
            f"{len(chunk):>8} "
            f"{chunk_memory:>15.2f}"
        )

        # Nie przechowujemy przetworzonych batchy
        del chunk

# Najwiekszy pojedynczy batch jako punkt porownania
memory_chunk = max(batch_memories)

total_batches = len(batch_memories)
total_rows = sum(batch_rows)

print(f"\nLiczba batchy: {total_batches}")
print(f"Przetworzone wiersze: {total_rows}")
print(f"Najwiekszy batch: {max(batch_rows)} wierszy")
print(f"Ostatni batch: {batch_rows[-1]} wierszy")
print(f"Pamiec pierwszego batcha: {batch_memories[0]:.2f} KiB")
print(f"Maksymalna pamiec batcha: {memory_chunk:.2f} KiB")
print(f"Srednia pamiec batcha: {np.mean(batch_memories):.2f} KiB")

# ==========================================================
# WARIANT 4 - OPTYMALIZACJA TYPOW
# ==========================================================

df_optimized = pd.read_csv(url)

# Sprawdzenie bezpieczenstwa konwersji do int8
int8_limits = np.iinfo(np.int8)

for column in int8_columns:

    if not df_optimized[column].between(
        int8_limits.min,
        int8_limits.max
    ).all():
        raise ValueError(
            f"Niebezpieczna konwersja kolumny {column}"
        )

    df_optimized[column] = (
        df_optimized[column].astype("int8")
    )

for column in category_columns:

    df_optimized[column] = (
        df_optimized[column].astype("category")
    )

memory_optimized = memory_kb(df_optimized)

print("\nWARIANT 4 - OPTYMALIZACJA TYPOW")
print("=" * 75)

print(f"Shape: {df_optimized.shape}")
print(f"Pamiec: {memory_optimized:.2f} KiB")

print("\nTypy danych po optymalizacji:")

print(df_optimized.dtypes.to_string())

# ==========================================================
# POROWNANIE TYPOW DANYCH
# ==========================================================

dtype_comparison = pd.DataFrame({
    "Typ_przed": df_full.dtypes.astype(str),
    "Typ_po": df_optimized.dtypes.astype(str)
})

print("\nPOROWNANIE TYPOW DANYCH")
print("=" * 75)

print(dtype_comparison.to_string())

# ==========================================================
# TABELA WYNIKOW
# ==========================================================

results = pd.DataFrame({
    "Metoda": [
        "Pelne wczytanie",
        "Usecols",
        "Chunksize=100",
        "Optymalizacja typow"
    ],
    "Pamięć (KB)": [
        memory_full,
        memory_selected,
        memory_chunk,
        memory_optimized
    ]
})

results["Oszczędność (%)"] = (
    (memory_full - results["Pamięć (KB)"])
    / memory_full * 100
)

print("\nPOROWNANIE ZUZYCIA PAMIECI")
print("=" * 75)

print(
    results.round(2).to_string(index=False)
)

# ==========================================================
# DODATKOWE STATYSTYKI
# ==========================================================

details = results.copy()

details["Oszczednosc_KiB"] = (
    memory_full - details["Pamięć (KB)"]
)

details["Stosunek_pamieci"] = (
    memory_full / details["Pamięć (KB)"]
)

print("\nSZCZEGOLOWE POROWNANIE")
print("=" * 75)

print(
    details.round(4).to_string(index=False)
)

# ==========================================================
# TEKSTOWY WYKRES ZUZYCIA PAMIECI
# ==========================================================

print("\nTEKSTOWY WYKRES ZUZYCIA PAMIECI")
print("=" * 75)

print("Legenda: jeden znak █ = okolo 10% maksymalnej pamieci")

max_memory = results["Pamięć (KB)"].max()

for _, row in results.iterrows():

    memory = row["Pamięć (KB)"]

    bar_length = round(
        memory / max_memory * 10
    )

    if memory > 0:
        bar_length = max(1, bar_length)

    bar = "█" * bar_length

    print(
        f"{row['Metoda']:<22} | "
        f"{bar:<10} "
        f"{memory:>8.2f} KiB"
    )

# ==========================================================
# TEKSTOWY WYKRES OSZCZEDNOSCI
# ==========================================================

print("\nTEKSTOWY WYKRES OSZCZEDNOSCI PAMIECI")
print("=" * 75)

print("Legenda: jeden znak █ = okolo 10 punktow procentowych")

for _, row in results.iterrows():

    saving = row["Oszczędność (%)"]

    bar_length = max(0, round(saving / 10))

    bar = "█" * bar_length

    print(
        f"{row['Metoda']:<22} | "
        f"{bar:<10} "
        f"{saving:>7.2f}%"
    )

# ==========================================================
# SZACOWANE OSZCZEDNOSCI ENERGII
# ==========================================================

energy = results.copy()

# Konwersja KiB na MiB
energy["Pamiec_MiB"] = (
    energy["Pamięć (KB)"] / 1024
)

energy["Oszczednosc_MiB"] = (
    memory_full - energy["Pamięć (KB)"]
) / 1024

# Szacowane zuzycie energii przez godzine
energy["Zuzycie_kWh_h"] = (
    energy["Pamiec_MiB"] * energy_factor
)

# Szacowana oszczednosc energii przez godzine
energy["Oszczednosc_kWh_h"] = (
    energy["Oszczednosc_MiB"] * energy_factor
)

# Przeliczenie na Wh
energy["Oszczednosc_Wh_h"] = (
    energy["Oszczednosc_kWh_h"] * 1000
)

# Dodatkowa symulacja pracy przez 24 godziny
energy["Oszczednosc_kWh_24h"] = (
    energy["Oszczednosc_kWh_h"] * 24
)

# Dodatkowa symulacja pracy przez 365 dni
energy["Oszczednosc_kWh_rok"] = (
    energy["Oszczednosc_kWh_h"] * 24 * 365
)

print("\nSZACOWANE OSZCZEDNOSCI ENERGII")
print("=" * 75)

print("Zalozenie dydaktyczne:")
print("1 MiB RAM = 0.0003 kWh/h")

print(
    energy[
        [
            "Metoda",
            "Pamiec_MiB",
            "Oszczednosc_MiB",
            "Zuzycie_kWh_h",
            "Oszczednosc_kWh_h",
            "Oszczednosc_Wh_h"
        ]
    ].round(8).to_string(index=False)
)

print("\nSYMULACJA DLUGOTERMINOWA")
print("=" * 75)

print(
    energy[
        [
            "Metoda",
            "Oszczednosc_kWh_24h",
            "Oszczednosc_kWh_rok"
        ]
    ].round(8).to_string(index=False)
)

print("\nUwaga:")
print("To model dydaktyczny, a nie rzeczywisty pomiar energii.")
print("Symulacja zaklada stale utrzymywanie danej ilosci RAM.")
print("Nie uwzglednia procesora, dysku ani czasu przetwarzania.")

# ==========================================================
# RANKING METOD
# ==========================================================

ranking = results.sort_values(
    "Pamięć (KB)",
    ascending=True
).reset_index(drop=True)

ranking.index = ranking.index + 1

print("\nRANKING EFEKTYWNOSCI PAMIECIOWEJ")
print("=" * 75)

print(ranking.round(2).to_string())

best_method = ranking.iloc[0]["Metoda"]

best_memory = ranking.iloc[0]["Pamięć (KB)"]

best_saving = ranking.iloc[0]["Oszczędność (%)"]

print(f"\nNajmniejsze zuzycie pamieci: {best_method}")
print(f"Pamiec: {best_memory:.2f} KiB")
print(f"Oszczednosc: {best_saving:.2f}%")

# ==========================================================
# POROWNANIE ZACHOWANYCH DANYCH
# ==========================================================

coverage = pd.DataFrame({
    "Metoda": results["Metoda"],
    "Wiersze_przetworzone": [
        len(df_full),
        len(df_selected),
        total_rows,
        len(df_optimized)
    ],
    "Liczba_kolumn": [
        len(df_full.columns),
        len(df_selected.columns),
        len(df_full.columns),
        len(df_optimized.columns)
    ],
    "Maks_wierszy_w_DataFrame": [
        len(df_full),
        len(df_selected),
        max(batch_rows),
        len(df_optimized)
    ]
})

print("\nPOROWNANIE ZAKRESU DANYCH")
print("=" * 75)

print(coverage.to_string(index=False))

# ==========================================================
# WNIOSKI
# ==========================================================

print("\nWNIOSKI")
print("=" * 75)

print("1. Pelne wczytanie stanowi punkt odniesienia.")
print("2. Usecols ogranicza liczbe wczytywanych kolumn.")
print("3. Batch processing ogranicza rozmiar pojedynczej partii.")
print("4. Batch processing nie wymaga laczenia wszystkich batchy.")
print("5. Optymalizacja typow zachowuje wszystkie dane.")
print("6. Typ int8 zajmuje mniej pamieci niz int64.")
print("7. Category jest korzystny dla powtarzalnych wartosci.")
print("8. Wybor metody zalezy od celu analizy.")
print("9. Pomiar dotyczy DataFrame, a nie calego procesu.")
print("10. Oszczednosci energii maja charakter dydaktyczny.")

# ==========================================================
# PODSUMOWANIE
# ==========================================================

print("\nPODSUMOWANIE")
print("=" * 75)

print(f"Liczba porownanych metod: {len(results)}")
print(f"Liczba pasazerow: {len(df_full)}")
print(f"Liczba batchy: {total_batches}")
print(f"Pelne wczytanie: {memory_full:.2f} KiB")
print(f"Usecols: {memory_selected:.2f} KiB")
print(f"Chunksize=100: {memory_chunk:.2f} KiB")
print(f"Optymalizacja typow: {memory_optimized:.2f} KiB")
print(f"Najlepsza metoda: {best_method}")
print(f"Maksymalna oszczednosc: {best_saving:.2f}%")

# ==========================================================
# AUTOMATYCZNA WERYFIKACJA
# ==========================================================

df_restored = df_optimized.astype(
    df_full.dtypes.to_dict()
)

tests = {
    "Dataset ma 891 wierszy":
        len(df_full) == 891,

    "Dataset ma 12 kolumn":
        len(df_full.columns) == 12,

    "Usecols zachowuje 891 wierszy":
        len(df_selected) == 891,

    "Usecols ma 5 kolumn":
        len(df_selected.columns) == 5,

    "Usecols zawiera wymagane kolumny":
        set(df_selected.columns) == set(selected_columns),

    "Usecols zachowuje wartosci":
        df_selected.equals(df_full[df_selected.columns]),

    "Utworzono 9 batchy":
        total_batches == 9,

    "Przetworzono wszystkie wiersze":
        total_rows == len(df_full),

    "Maksymalny batch ma 100 wierszy":
        max(batch_rows) == 100,

    "Ostatni batch ma 91 wierszy":
        batch_rows[-1] == 91,

    "Pamiec batcha jest poprawna":
        np.isclose(memory_chunk, max(batch_memories)),

    "Optymalizacja zachowuje shape":
        df_optimized.shape == df_full.shape,

    "Wymagane kolumny maja typ int8":
        all(
            str(df_optimized[col].dtype) == "int8"
            for col in int8_columns
        ),

    "Wymagane kolumny maja typ category":
        all(
            str(df_optimized[col].dtype) == "category"
            for col in category_columns
        ),

    "Optymalizacja zachowuje wartosci":
        df_restored.equals(df_full),

    "Optymalizacja zachowuje NaN":
        df_optimized.isna().equals(df_full.isna()),

    "Usecols zmniejsza pamiec":
        memory_selected < memory_full,

    "Chunksize zmniejsza pamiec":
        memory_chunk < memory_full,

    "Optymalizacja zmniejsza pamiec":
        memory_optimized < memory_full,

    "Porownano 4 metody":
        len(results) == 4,

    "Pelne wczytanie ma 0% oszczednosci":
        np.isclose(results.iloc[0]["Oszczędność (%)"], 0),

    "Oszczednosci sa w zakresie 0-100%":
        results["Oszczędność (%)"].between(0, 100).all(),

    "Oszczednosci pamieci sa poprawne":
        np.allclose(
            results["Oszczędność (%)"],
            (memory_full - results["Pamięć (KB)"])
            / memory_full * 100
        ),

    "Oszczednosci energii sa poprawne":
        np.allclose(
            energy["Oszczednosc_kWh_h"],
            (memory_full - results["Pamięć (KB)"])
            / 1024 * energy_factor
        ),

    "Oszczednosci energii sa nieujemne":
        energy["Oszczednosc_kWh_h"].ge(0).all(),

    "Ranking jest poprawny":
        ranking["Pamięć (KB)"].is_monotonic_increasing,

    "Oryginalne dane pozostaly niezmienione":
        df_full.equals(df_original)
}

print("\nWERYFIKACJA")
print("=" * 75)

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

assert all(tests.values()), "Nie wszystkie testy zostaly zaliczone."

print("Wszystkie testy zakonczone pomyslnie.")
