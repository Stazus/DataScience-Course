# Lekcja 11 - Zadanie 3: Selekcja kolumn

import pandas as pd


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia oryginalnego DataFrame
df_original = df.copy()

# Lista wybranych kolumn
kolumny = ["Name", "Age", "Sex", "Survived"]

# Utworzenie nowego DataFrame
df_subset = df[kolumny].copy()

# Nazwa pliku wynikowego
plik_csv = "titanic_subset.csv"

# Zapis do pliku CSV bez dodatkowego indeksu
df_subset.to_csv(plik_csv, index=False, encoding="utf-8")

# Ponowne wczytanie zapisanego pliku
df_saved = pd.read_csv(plik_csv)

print("SELEKCJA KOLUMN - DATASET TITANIC")
print("=" * 75)

print("\nORYGINALNY DATAFRAME")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba wierszy: {df.shape[0]}")
print(f"Liczba kolumn: {df.shape[1]}")
print(f"Kolumny: {df.columns.tolist()}")

print("\nNOWY DATAFRAME")
print("=" * 75)
print(f"Shape: {df_subset.shape}")
print(f"Liczba wierszy: {df_subset.shape[0]}")
print(f"Liczba kolumn: {df_subset.shape[1]}")
print(f"Kolumny: {df_subset.columns.tolist()}")

print("\nPIERWSZE 10 WIERSZY")
print("=" * 75)
print(df_subset.head(10).to_string(index=False))

print("\nTYPY DANYCH")
print("=" * 75)
print(df_subset.dtypes.to_string())

print("\nBRAKUJACE WARTOSCI")
print("=" * 75)
print(df_subset.isna().sum().to_string())

print("\nZAPIS DO PLIKU CSV")
print("=" * 75)
print(f"Nazwa pliku: {plik_csv}")
print(f"Shape zapisanego datasetu: {df_saved.shape}")
print("Plik CSV zapisany i ponownie wczytany.")

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Liczba kolumn przed selekcja: {df.shape[1]}")
print(f"Liczba kolumn po selekcji: {df_subset.shape[1]}")
print(f"Liczba pominietych kolumn: {df.shape[1] - df_subset.shape[1]}")
print(f"Liczba zachowanych wierszy: {len(df_subset)}")

print("\nWERYFIKACJA")
print("=" * 75)
print(f"Czy oryginalny dataset ma 891 wierszy: {len(df) == 891}")
print(f"Czy oryginalny dataset ma 12 kolumn: {df.shape[1] == 12}")
print(f"Czy nowy DataFrame ma ksztalt (891, 4): {df_subset.shape == (891, 4)}")
print(f"Czy wybrano poprawne kolumny: {df_subset.columns.tolist() == kolumny}")
print(f"Czy zachowano liczbe wierszy: {len(df_subset) == len(df)}")
print(f"Czy dane wybranych kolumn sa poprawne: {df_subset.equals(df[kolumny])}")
print(f"Czy zapisany CSV ma poprawny ksztalt: {df_saved.shape == df_subset.shape}")
print(f"Czy zapisany CSV ma poprawne kolumny: {df_saved.columns.tolist() == kolumny}")
print(f"Czy zapisane dane sa zgodne: {df_saved.equals(df_subset)}")
print(f"Czy oryginalny DataFrame pozostal niezmieniony: {df.equals(df_original)}")
