# Lekcja 11 - Zadanie 6: Wypelnianie NaN srednia

import pandas as pd
import numpy as np


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia oryginalnych danych
df_original = df.copy()

# Maska brakujacych wartosci wieku
maska_nan = df["Age"].isna()

# Liczba brakow przed uzupelnieniem
braki_przed = df["Age"].isna().sum()

# Obliczenie sredniego wieku z pominieciem NaN
sredni_wiek = df["Age"].mean()

# Kopia DataFrame do uzupelnienia danych
df_filled = df.copy()

# Wypelnienie brakujacych wartosci srednia
df_filled["Age"] = df_filled["Age"].fillna(sredni_wiek)

# Liczba brakow po uzupelnieniu
braki_po = df_filled["Age"].isna().sum()

print("WYPELNIANIE NaN SREDNIA - DATASET TITANIC")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Znany wiek: {df['Age'].count()}")
print(f"Brakujacy wiek: {braki_przed}")

print("\nOBLICZENIE SREDNIEGO WIEKU")
print("=" * 75)
print(f"Sredni wiek: {sredni_wiek:.4f} lat")

print("\nSTATYSTYKI PRZED UZUPELNIENIEM")
print("=" * 75)
print(df["Age"].describe().round(4).to_string())

print("\nSTATYSTYKI PO UZUPELNIENIU")
print("=" * 75)
print(df_filled["Age"].describe().round(4).to_string())

# Porownanie przykladowych uzupelnionych rekordow
porownanie = pd.DataFrame({
    "Name": df.loc[maska_nan, "Name"],
    "Age_przed": df.loc[maska_nan, "Age"],
    "Age_po": df_filled.loc[maska_nan, "Age"]
})

print("\nPIERWSZE 10 UZUPELNIONYCH REKORDOW")
print("=" * 75)
print(porownanie.head(10).round(4).to_string(index=False))

print("\nPOROWNANIE BRAKUJACYCH DANYCH")
print("=" * 75)
print(f"NaN przed: {braki_przed}")
print(f"NaN po: {braki_po}")
print(f"Uzupelnione wartosci: {braki_przed - braki_po}")

print("\nTEKSTOWY WYKRES BRAKOW")
print("=" * 75)
print("Legenda: jeden znak = okolo 5 brakow")
print(f"Przed | {'█' * round(braki_przed / 5)} ({braki_przed})")
print(f"Po    | {'█' * round(braki_po / 5)} ({braki_po})")

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Liczba pasazerow: {len(df_filled)}")
print(f"Sredni wiek przed: {sredni_wiek:.4f}")
print(f"Sredni wiek po: {df_filled['Age'].mean():.4f}")
print(f"Odchylenie przed: {df['Age'].std():.4f}")
print(f"Odchylenie po: {df_filled['Age'].std():.4f}")
print(f"Pozostale NaN w Age: {braki_po}")

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy dataset ma 891 wierszy: {len(df) == 891}")
print(f"Czy poczatkowo bylo 177 brakow: {braki_przed == 177}")
print(f"Czy sredni wiek jest poprawny: {np.isclose(sredni_wiek, 29.69911764705882)}")
print(f"Czy nie ma juz NaN w Age: {braki_po == 0}")
print(f"Czy uzupelniono 177 wartosci: {braki_przed - braki_po == 177}")
print(f"Czy uzupelniono braki srednia: {np.allclose(df_filled.loc[maska_nan, 'Age'], sredni_wiek)}")
print(f"Czy srednia pozostala niezmieniona: {np.isclose(df_filled['Age'].mean(), sredni_wiek)}")
print(f"Czy zachowano znane wartosci wieku: {df_filled.loc[~maska_nan, 'Age'].equals(df.loc[~maska_nan, 'Age'])}")
print(f"Czy zachowano ksztalt DataFrame: {df_filled.shape == df.shape}")
print(f"Czy pozostale kolumny sa niezmienione: {df_filled.drop(columns='Age').equals(df.drop(columns='Age'))}")
print(f"Czy oryginalne dane pozostaly niezmienione: {df.equals(df_original)}")
