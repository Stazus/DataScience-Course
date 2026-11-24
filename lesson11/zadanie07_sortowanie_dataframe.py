# Lekcja 11 - Zadanie 7: Sortowanie DataFrame

import pandas as pd


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia oryginalnych danych
df_original = df.copy()

# Liczba brakujacych wartosci wieku
braki_wieku = df["Age"].isna().sum()

# Wybor pasazerow ze znanym wiekiem
df_known = df.dropna(subset=["Age"]).copy()

# Sortowanie wedlug wieku rosnaco
df_sorted = df_known.sort_values(
    by="Age",
    ascending=True
)

# Wybor kolumn do wyswietlenia
kolumny = ["PassengerId", "Name", "Age", "Sex", "Survived"]

# 10 najmlodszych pasazerow
najmlodsi = df_sorted[kolumny].head(10)

# 10 najstarszych pasazerow
najstarsi = df_sorted[kolumny].tail(10).sort_values(
    by="Age",
    ascending=False
)

print("SORTOWANIE DATAFRAME - DATASET TITANIC")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Znany wiek: {len(df_known)}")
print(f"Brakujacy wiek: {braki_wieku}")

print("\nSORTOWANIE DANYCH")
print("=" * 75)
print("Kolumna sortowania: Age")
print("Kierunek: rosnaco")
print(f"Shape po sortowaniu: {df_sorted.shape}")

print("\n10 NAJMLODSZYCH PASAZEROW")
print("=" * 75)
print(najmlodsi.to_string(index=False))

print("\n10 NAJSTARSZYCH PASAZEROW")
print("=" * 75)
print(najstarsi.to_string(index=False))

print("\nSTATYSTYKI NAJMLODSZYCH PASAZEROW")
print("=" * 75)
print(f"Sredni wiek: {najmlodsi['Age'].mean():.2f}")
print(f"Minimalny wiek: {najmlodsi['Age'].min():.2f}")
print(f"Maksymalny wiek: {najmlodsi['Age'].max():.2f}")

print("\nSTATYSTYKI NAJSTARSZYCH PASAZEROW")
print("=" * 75)
print(f"Sredni wiek: {najstarsi['Age'].mean():.2f}")
print(f"Minimalny wiek: {najstarsi['Age'].min():.2f}")
print(f"Maksymalny wiek: {najstarsi['Age'].max():.2f}")

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Liczba wszystkich pasazerow: {len(df)}")
print(f"Liczba posortowanych pasazerow: {len(df_sorted)}")
print(f"Liczba pominietych rekordow: {braki_wieku}")
print(f"Najmlodszy pasazer: {df_sorted['Age'].min():.2f} lat")
print(f"Najstarszy pasazer: {df_sorted['Age'].max():.2f} lat")
print(f"Roznica wieku: {df_sorted['Age'].max() - df_sorted['Age'].min():.2f} lat")

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy dataset ma 891 wierszy: {len(df) == 891}")
print(f"Czy znany wiek ma 714 pasazerow: {len(df_known) == 714}")
print(f"Czy pominieto 177 brakow: {braki_wieku == 177}")
print(f"Czy dane sa posortowane rosnaco: {df_sorted['Age'].is_monotonic_increasing}")
print(f"Czy wybrano 10 najmlodszych: {len(najmlodsi) == 10}")
print(f"Czy wybrano 10 najstarszych: {len(najstarsi) == 10}")
print(f"Czy najmlodsi sa posortowani rosnaco: {najmlodsi['Age'].is_monotonic_increasing}")
print(f"Czy najstarsi sa posortowani malejaco: {najstarsi['Age'].is_monotonic_decreasing}")
print(f"Czy najmlodszy ma 0.42 lat: {najmlodsi['Age'].min() == 0.42}")
print(f"Czy najstarszy ma 80 lat: {najstarsi['Age'].max() == 80}")
print(f"Czy brak NaN w posortowanym wieku: {not df_sorted['Age'].isna().any()}")
print(f"Czy sortowanie zachowalo wszystkie znane rekordy: {df_sorted.sort_index().equals(df_known)}")
print(f"Czy oryginalne dane pozostaly niezmienione: {df.equals(df_original)}")
