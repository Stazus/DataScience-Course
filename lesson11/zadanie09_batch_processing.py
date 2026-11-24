# Lekcja 11 - Zadanie 9: Batch processing

import pandas as pd
import numpy as np


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Rozmiar pojedynczej partii
batch_size = 100

# Akumulatory
age_sum = 0.0
age_count = 0
total_rows = 0
total_batches = 0

# Lista statystyk poszczegolnych partii
batch_stats = []

print("BATCH PROCESSING - DATASET TITANIC")
print("=" * 75)

print("\nKONFIGURACJA")
print("=" * 75)
print(f"Rozmiar batcha: {batch_size}")
print("Metoda: pd.read_csv(chunksize=100)")

# Wczytywanie danych partiami
for batch_number, batch in enumerate(
    pd.read_csv(url, chunksize=batch_size),
    start=1
):
    # Statystyki pojedynczego batcha
    batch_rows = len(batch)
    batch_age_sum = batch["Age"].sum()
    batch_age_count = batch["Age"].count()
    batch_age_mean = batch["Age"].mean()
    batch_missing = batch["Age"].isna().sum()

    # Aktualizacja akumulatorow
    age_sum += batch_age_sum
    age_count += batch_age_count
    total_rows += batch_rows
    total_batches += 1

    # Zapis statystyk batcha
    batch_stats.append({
        "Batch": batch_number,
        "Wiersze": batch_rows,
        "Znany_wiek": batch_age_count,
        "Brakujacy_wiek": batch_missing,
        "Suma_wieku": batch_age_sum,
        "Sredni_wiek": batch_age_mean
    })

# Obliczenie globalnej sredniej
global_mean = age_sum / age_count

# DataFrame ze statystykami batchy
df_stats = pd.DataFrame(batch_stats)

print("\nSTATYSTYKI POSZCZEGOLNYCH BATCHY")
print("=" * 75)
print(df_stats.round(4).to_string(index=False))

print("\nGLOBALNE STATYSTYKI")
print("=" * 75)
print(f"Liczba batchy: {total_batches}")
print(f"Liczba wszystkich wierszy: {total_rows}")
print(f"Liczba znanych wartosci wieku: {age_count}")
print(f"Liczba brakujacych wartosci: {total_rows - age_count}")
print(f"Suma wieku: {age_sum:.4f}")
print(f"Globalna srednia wieku: {global_mean:.4f} lat")

print("\nTEKSTOWY WYKRES SREDNIEGO WIEKU")
print("=" * 75)
print("Legenda: jeden znak = okolo 1 roku")

for _, row in df_stats.iterrows():
    srednia = row["Sredni_wiek"]
    slupek = "█" * round(srednia)

    print(
        f"Batch {int(row['Batch']):2d} | "
        f"{slupek:35s} {srednia:.2f}"
    )

# Porownanie ze zwykla srednia srednich
mean_of_means = df_stats["Sredni_wiek"].mean()

print("\nPOROWNANIE METOD OBLICZANIA SREDNIEJ")
print("=" * 75)
print(f"Globalna srednia: {global_mean:.4f}")
print(f"Srednia srednich batchy: {mean_of_means:.4f}")
print(f"Roznica: {abs(global_mean - mean_of_means):.6f}")

print("\nWERYFIKACJA")
print("=" * 75)
print(f"Czy przetworzono 891 wierszy: {total_rows == 891}")
print(f"Czy utworzono 9 batchy: {total_batches == 9}")
print(f"Czy pierwsze 8 batchy ma po 100 wierszy: {(df_stats['Wiersze'].iloc[:8] == 100).all()}")
print(f"Czy ostatni batch ma 91 wierszy: {df_stats['Wiersze'].iloc[-1] == 91}")
print(f"Czy znany wiek ma 714 pasazerow: {age_count == 714}")
print(f"Czy brakuje 177 wartosci wieku: {total_rows - age_count == 177}")
print(f"Czy suma wierszy jest poprawna: {df_stats['Wiersze'].sum() == total_rows}")
print(f"Czy suma wieku jest poprawna: {np.isclose(df_stats['Suma_wieku'].sum(), age_sum)}")
print(f"Czy liczba znanych wartosci jest poprawna: {df_stats['Znany_wiek'].sum() == age_count}")
print(f"Czy globalna srednia jest poprawna: {np.isclose(global_mean, 29.69911764705882)}")
print(f"Czy globalna srednia jest skonczona: {np.isfinite(global_mean)}")
print(f"Czy wszystkie srednie batchy sa skonczone: {np.isfinite(df_stats['Sredni_wiek']).all()}")
