# Lekcja 11 - Zadanie 15: Custom aggregation podczas batch loading

import pandas as pd
import numpy as np


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Konfiguracja batch processing
batch_size = 50

# Zmienne akumulacyjne
total_passengers = 0
age_sum = 0.0
age_count = 0
survived_sum = 0
total_batches = 0

# Monitorowanie pamieci
max_batch_memory = 0
max_batch_rows = 0
last_batch_rows = 0

print("CUSTOM AGGREGATION - BATCH LOADING TITANIC")
print("=" * 75)

print("\nKONFIGURACJA")
print("=" * 75)
print(f"Rozmiar batcha: {batch_size}")
print("Metoda: pd.read_csv(chunksize=50)")
print("Bez konkatenacji batchy")

print("\nPRZETWARZANIE POSZCZEGOLNYCH BATCHY")
print("=" * 75)

print(
    f"{'Batch':>5} "
    f"{'Wiersze':>8} "
    f"{'Znany wiek':>12} "
    f"{'Ocalali':>8} "
    f"{'Pamiec KiB':>12}"
)

# Przetwarzanie danych partiami
with pd.read_csv(url, chunksize=batch_size) as reader:

    for batch in reader:

        # Statystyki pojedynczego batcha
        batch_rows = len(batch)
        batch_age_sum = batch["Age"].sum()
        batch_age_count = batch["Age"].count()
        batch_survived = batch["Survived"].sum()

        # Akumulacja wynikow
        total_passengers += batch_rows
        age_sum += batch_age_sum
        age_count += batch_age_count
        survived_sum += batch_survived
        total_batches += 1

        # Zuzycie pamieci pojedynczego batcha
        batch_memory = batch.memory_usage(deep=True).sum()

        max_batch_memory = max(
            max_batch_memory,
            batch_memory
        )

        max_batch_rows = max(max_batch_rows, batch_rows)
        last_batch_rows = batch_rows

        print(
            f"{total_batches:>5} "
            f"{batch_rows:>8} "
            f"{batch_age_count:>12} "
            f"{batch_survived:>8} "
            f"{batch_memory / 1024:>12.2f}"
        )

        # Zwolnienie referencji do przetworzonego batcha
        del batch

# Obliczenie globalnych agregacji
avg_age = age_sum / age_count
survival_rate = survived_sum / total_passengers

print("\nGLOBALNE STATYSTYKI - BATCH PROCESSING")
print("=" * 75)
print(f"Liczba batchy: {total_batches}")
print(f"Liczba pasazerow: {total_passengers}")
print(f"Liczba znanych wartosci wieku: {age_count}")
print(f"Liczba brakujacych wartosci wieku: {total_passengers - age_count}")
print(f"Suma wieku: {age_sum:.4f}")
print(f"Sredni wiek: {avg_age:.4f}")
print(f"Liczba ocalalych: {survived_sum}")
print(f"Wskaznik przezycia: {survival_rate:.4f}")
print(f"Przezywalnosc: {survival_rate:.2%}")

# Wczytanie pelnego DataFrame wylacznie do porownania
df_full = pd.read_csv(url)

# Agregacje dla pelnego DataFrame
full_passengers = len(df_full)
full_age_sum = df_full["Age"].sum()
full_age_count = df_full["Age"].count()
full_avg_age = df_full["Age"].mean()
full_survived = df_full["Survived"].sum()
full_survival_rate = df_full["Survived"].mean()

# Zuzycie pamieci pelnego DataFrame
full_memory = df_full.memory_usage(deep=True).sum()

# Porownanie wynikow
comparison = pd.DataFrame({
    "Batch_processing": [
        total_passengers,
        age_count,
        age_sum,
        avg_age,
        survived_sum,
        survival_rate * 100
    ],
    "Full_DataFrame": [
        full_passengers,
        full_age_count,
        full_age_sum,
        full_avg_age,
        full_survived,
        full_survival_rate * 100
    ]
}, index=[
    "Liczba_pasazerow",
    "Znany_wiek",
    "Suma_wieku",
    "Sredni_wiek",
    "Ocalali",
    "Przezywalnosc_%"
])

comparison["Roznica"] = (
    comparison["Batch_processing"]
    - comparison["Full_DataFrame"]
)

print("\nPOROWNANIE METOD AGREGACJI")
print("=" * 75)
print(comparison.to_string(float_format=lambda x: f"{x:.4f}"))

# Obliczenie redukcji pamieci DataFrame
memory_saved = full_memory - max_batch_memory

memory_reduction = (
    memory_saved / full_memory * 100
)

memory_ratio = full_memory / max_batch_memory

print("\nPOROWNANIE ZUZYCIA PAMIECI DATAFRAME")
print("=" * 75)
print(f"Najwiekszy batch: {max_batch_memory} B")
print(f"Najwiekszy batch: {max_batch_memory / 1024:.2f} KiB")
print(f"Pelny DataFrame: {full_memory} B")
print(f"Pelny DataFrame: {full_memory / 1024:.2f} KiB")
print(f"Oszczednosc: {memory_saved / 1024:.2f} KiB")
print(f"Redukcja pamieci: {memory_reduction:.2f}%")
print(f"Stosunek zuzycia pamieci: {memory_ratio:.2f}x")

# Tekstowa wizualizacja zuzycia pamieci
print("\nTEKSTOWY WYKRES ZUZYCIA PAMIECI")
print("=" * 75)
print("Skala wzgledem pelnego DataFrame")

for name, memory in [
    ("Full DataFrame", full_memory),
    ("Batch", max_batch_memory)
]:
    bar_length = round(memory / full_memory * 50)
    bar = "█" * bar_length

    print(
        f"{name:<15} | "
        f"{bar:<50} "
        f"{memory / 1024:.2f} KiB"
    )

print("\nWNIOSKI")
print("=" * 75)
print("1. Batch processing nie wymaga laczenia wszystkich batchy.")
print("2. Akumulatory pozwalaja obliczyc globalne statystyki.")
print("3. Srednia wieku uwzglednia tylko znane wartosci.")
print("4. Obie metody zwracaja takie same statystyki.")
print("5. Pojedynczy batch zajmuje mniej pamieci.")
print("6. Pomiar dotyczy pamieci DataFrame, a nie calego procesu.")

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Liczba batchy: {total_batches}")
print(f"Maksymalny rozmiar batcha: {max_batch_rows}")
print(f"Rozmiar ostatniego batcha: {last_batch_rows}")
print(f"Liczba pasazerow: {total_passengers}")
print(f"Sredni wiek: {avg_age:.4f}")
print(f"Przezywalnosc: {survival_rate:.2%}")
print(f"Redukcja pamieci DataFrame: {memory_reduction:.2f}%")

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy przetworzono 891 pasazerow: {total_passengers == 891}")
print(f"Czy utworzono 18 batchy: {total_batches == 18}")
print(f"Czy maksymalny batch ma 50 wierszy: {max_batch_rows == 50}")
print(f"Czy ostatni batch ma 41 wierszy: {last_batch_rows == 41}")
print(f"Czy znany wiek ma 714 pasazerow: {age_count == 714}")
print(f"Czy brakuje 177 wartosci wieku: {total_passengers - age_count == 177}")
print(f"Czy liczba ocalalych wynosi 342: {survived_sum == 342}")
print(f"Czy liczba pasazerow jest zgodna: {total_passengers == full_passengers}")
print(f"Czy liczba znanych wartosci wieku jest zgodna: {age_count == full_age_count}")
print(f"Czy suma wieku jest zgodna: {np.isclose(age_sum, full_age_sum)}")
print(f"Czy srednia wieku jest zgodna: {np.isclose(avg_age, full_avg_age)}")
print(f"Czy liczba ocalalych jest zgodna: {survived_sum == full_survived}")
print(f"Czy przezywalnosc jest zgodna: {np.isclose(survival_rate, full_survival_rate)}")
print(f"Czy wszystkie agregacje sa zgodne: {np.allclose(comparison['Batch_processing'], comparison['Full_DataFrame'])}")
print(f"Czy zmniejszono zuzycie pamieci: {max_batch_memory < full_memory}")
print(f"Czy redukcja pamieci jest poprawna: {0 < memory_reduction < 100}")
print(f"Czy wskaznik przezycia jest poprawny: {0 <= survival_rate <= 1}")
