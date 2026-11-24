# Lekcja 11 - Zadanie 10: Kompleksowe czyszczenie danych

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

# DataFrame przeznaczony do czyszczenia
df_clean = df.copy()

# Statystyki przed czyszczeniem
shape_przed = df.shape
nan_przed = df.isna().sum().sum()
age_stats_przed = df["Age"].describe()

print("KOMPLEKSOWE CZYSZCZENIE DANYCH - TITANIC")
print("=" * 75)

print("\nDANE PRZED CZYSZCZENIEM")
print("=" * 75)
print(f"Shape: {shape_przed}")
print(f"Liczba wierszy: {len(df)}")
print(f"Liczba kolumn: {df.shape[1]}")
print(f"Liczba wszystkich NaN: {nan_przed}")

print("\nBRAKUJACE WARTOSCI PRZED CZYSZCZENIEM")
print("=" * 75)
print(df.isna().sum().to_string())

# ETAP 1 - Usuniecie kolumn z ponad 60% NaN
prog = 60

procent_nan = df_clean.isna().mean() * 100

kolumny_do_usuniecia = procent_nan[
    procent_nan > prog
].index.tolist()

df_clean = df_clean.drop(columns=kolumny_do_usuniecia)

nan_etap1 = df_clean.isna().sum().sum()

print("\nETAP 1 - USUWANIE KOLUMN")
print("=" * 75)
print(f"Prog brakow: {prog}%")
print(f"Usuniete kolumny: {kolumny_do_usuniecia}")
print(f"Shape: {df_clean.shape}")
print(f"Pozostale NaN: {nan_etap1}")

# ETAP 2 - Uzupelnienie Age mediana
mediana_wieku = df_clean["Age"].median()
braki_age = df_clean["Age"].isna().sum()

df_clean["Age"] = df_clean["Age"].fillna(mediana_wieku)

nan_etap2 = df_clean.isna().sum().sum()

print("\nETAP 2 - UZUPELNIANIE AGE MEDIANA")
print("=" * 75)
print(f"Mediana wieku: {mediana_wieku:.2f}")
print(f"Uzupelnione wartosci: {braki_age}")
print(f"Pozostale NaN w Age: {df_clean['Age'].isna().sum()}")
print(f"Pozostale NaN w DataFrame: {nan_etap2}")

# ETAP 3 - Uzupelnienie Embarked dominanta
dominanta_embarked = df_clean["Embarked"].mode().iloc[0]
braki_embarked = df_clean["Embarked"].isna().sum()

df_clean["Embarked"] = df_clean["Embarked"].fillna(
    dominanta_embarked
)

nan_etap3 = df_clean.isna().sum().sum()

print("\nETAP 3 - UZUPELNIANIE EMBARKED DOMINANTA")
print("=" * 75)
print(f"Dominanta Embarked: {dominanta_embarked}")
print(f"Uzupelnione wartosci: {braki_embarked}")
print(f"Pozostale NaN: {nan_etap3}")

# ETAP 4 - Usuniecie wierszy z pozostalymi NaN
wiersze_przed_dropna = len(df_clean)

df_clean = df_clean.dropna()

usuniete_wiersze = wiersze_przed_dropna - len(df_clean)

# Statystyki po czyszczeniu
shape_po = df_clean.shape
nan_po = df_clean.isna().sum().sum()
age_stats_po = df_clean["Age"].describe()

print("\nETAP 4 - USUWANIE POZOSTALYCH NaN")
print("=" * 75)
print(f"Usuniete wiersze: {usuniete_wiersze}")
print(f"Shape: {shape_po}")
print(f"Pozostale NaN: {nan_po}")

print("\nPOROWNANIE STATYSTYK AGE")
print("=" * 75)

porownanie = pd.DataFrame({
    "Przed": age_stats_przed,
    "Po": age_stats_po
})

porownanie["Roznica"] = (
    porownanie["Po"] - porownanie["Przed"]
)

print(porownanie.round(4).to_string())

print("\nTEKSTOWY WYKRES BRAKUJACYCH DANYCH")
print("=" * 75)
print("Legenda: jeden znak = okolo 20 brakow")

etapy = {
    "Przed": nan_przed,
    "Etap 1": nan_etap1,
    "Etap 2": nan_etap2,
    "Etap 3": nan_etap3,
    "Etap 4": nan_po
}

for nazwa, liczba in etapy.items():
    dlugosc = int(np.ceil(liczba / 20))
    slupek = "█" * dlugosc

    print(f"{nazwa:8s} | {slupek:45s} {liczba}")

print("\nPIERWSZE 5 WIERSZY OCZYSZCZONYCH DANYCH")
print("=" * 75)
print(df_clean.head().to_string(index=False))

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Shape przed: {shape_przed}")
print(f"Shape po: {shape_po}")
print(f"Usuniete kolumny: {len(kolumny_do_usuniecia)}")
print(f"Usuniete wiersze: {len(df) - len(df_clean)}")
print(f"NaN przed: {nan_przed}")
print(f"NaN po: {nan_po}")
print(f"Usuniete lub uzupelnione NaN: {nan_przed - nan_po}")
print(f"Zachowane rekordy: {len(df_clean) / len(df) * 100:.2f}%")

print("\nWERYFIKACJA")
print("=" * 75)
print(f"Czy oryginalny dataset ma ksztalt (891, 12): {shape_przed == (891, 12)}")
print(f"Czy poczatkowo bylo 866 NaN: {nan_przed == 866}")
print(f"Czy usunieto tylko Cabin: {kolumny_do_usuniecia == ['Cabin']}")
print(f"Czy mediana wieku wynosi 28: {np.isclose(mediana_wieku, 28)}")
print(f"Czy dominanta Embarked to S: {dominanta_embarked == 'S'}")
print(f"Czy uzupelniono 177 brakow Age: {braki_age == 177}")
print(f"Czy uzupelniono 2 braki Embarked: {braki_embarked == 2}")
print(f"Czy nie ma NaN w Age: {df_clean['Age'].notna().all()}")
print(f"Czy nie ma NaN w Embarked: {df_clean['Embarked'].notna().all()}")
print(f"Czy nie ma zadnych NaN: {nan_po == 0}")
print(f"Czy zachowano wszystkie wiersze: {len(df_clean) == 891}")
print(f"Czy wynik ma ksztalt (891, 11): {shape_po == (891, 11)}")
print(f"Czy znane wartosci wieku pozostaly niezmienione: {df_clean.loc[df['Age'].notna(), 'Age'].equals(df['Age'].dropna())}")
print(f"Czy oryginalne dane pozostaly niezmienione: {df.equals(df_original)}")
