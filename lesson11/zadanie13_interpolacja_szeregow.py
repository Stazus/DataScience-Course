# Lekcja 11 - Zadanie 13: Interpolacja szeregow czasowych

import pandas as pd
import numpy as np


# Generowanie szeregu czasowego - 20 dni
daty = pd.date_range(
    start="2026-01-01",
    periods=20,
    freq="D"
)

# Przykladowe wartosci z brakami
wartosci = [
    10, 12, np.nan, 16, 18,
    np.nan, np.nan, 24, 22, 20,
    np.nan, 26, 28, 30, np.nan,
    34, 32, np.nan, 36, 38
]

# Utworzenie DataFrame z indeksem czasowym
df = pd.DataFrame(
    {"Oryginal": wartosci},
    index=daty
)

df.index.name = "Data"

# Kopia oryginalnych danych
df_original = df.copy()

# Maska brakujacych wartosci
maska_nan = df["Oryginal"].isna()

print("INTERPOLACJA SZEREGOW CZASOWYCH")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba dni: {len(df)}")
print(f"Data poczatkowa: {df.index.min().date()}")
print(f"Data koncowa: {df.index.max().date()}")
print(f"Liczba znanych wartosci: {df['Oryginal'].count()}")
print(f"Liczba NaN: {maska_nan.sum()}")
print(f"Procent brakow: {maska_nan.mean() * 100:.2f}%")

# DataFrame do porownania metod
df_result = df.copy()

# Metoda 1 - forward fill
df_result["FFill"] = df["Oryginal"].ffill()

# Metoda 2 - backward fill
df_result["BFill"] = df["Oryginal"].bfill()

# Metoda 3 - interpolacja liniowa
df_result["Linear"] = df["Oryginal"].interpolate(
    method="linear"
)

print("\nPOROWNANIE CZTERECH WERSJI DANYCH")
print("=" * 75)
print(df_result.round(2).to_string())

print("\nTYLKO UZUPELNIONE WARTOSCI")
print("=" * 75)
print(df_result.loc[maska_nan].round(2).to_string())

# Porownanie liczby brakow
raport_nan = pd.DataFrame({
    "Liczba_NaN": df_result.isna().sum(),
    "Procent_NaN": df_result.isna().mean() * 100
})

print("\nBRAKUJACE WARTOSCI")
print("=" * 75)
print(raport_nan.round(2).to_string())

# Porownanie statystyk
print("\nSTATYSTYKI POSZCZEGOLNYCH METOD")
print("=" * 75)
print(df_result.describe().round(4).to_string())

# Funkcja generujaca tekstowy slupek
def tekstowy_slupek(wartosc):
    if pd.isna(wartosc):
        return "NaN"

    return "█" * int(round(wartosc / 2))


# Wizualizacja tekstowa wszystkich czterech wersji
print("\nTEKSTOWA WIZUALIZACJA SZEREGOW")
print("=" * 75)
print("Legenda: jeden znak █ = okolo 2 jednostek")

for kolumna in df_result.columns:

    print(f"\nMETODA: {kolumna}")
    print("-" * 75)

    for data, wartosc in df_result[kolumna].items():

        slupek = tekstowy_slupek(wartosc)

        if pd.isna(wartosc):
            etykieta = "NaN"
        else:
            etykieta = f"{wartosc:.2f}"

        oznaczenie = "*" if maska_nan.loc[data] else " "

        print(
            f"{data.date()} {oznaczenie} | "
            f"{slupek:20} {etykieta}"
        )

print("\n* - miejsce brakujacej wartosci w oryginale")

# Porownanie metod dla uzupelnionych rekordow
df_missing = df_result.loc[
    maska_nan,
    ["FFill", "BFill", "Linear"]
].copy()

df_missing["Roznica_FFill_BFill"] = (
    df_missing["FFill"] - df_missing["BFill"]
).abs()

print("\nPOROWNANIE UZUPELNIEN")
print("=" * 75)
print(df_missing.round(4).to_string())

# Sprawdzenie, czy znane wartosci pozostaly niezmienione
znane_wartosci = ~maska_nan

zachowano_wartosci = all(
    df_result.loc[znane_wartosci, kolumna].equals(
        df.loc[znane_wartosci, "Oryginal"]
    )
    for kolumna in ["FFill", "BFill", "Linear"]
)

# Interpolacja powinna znajdowac sie pomiedzy
# poprzednia i nastepna znana wartoscia
dolna_granica = df_missing[["FFill", "BFill"]].min(axis=1)
gorna_granica = df_missing[["FFill", "BFill"]].max(axis=1)

interpolacja_poprawna = (
    df_missing["Linear"].ge(dolna_granica)
    & df_missing["Linear"].le(gorna_granica)
).all()

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Liczba dni: {len(df_result)}")
print(f"Shape przed: {df.shape}")
print(f"Shape po: {df_result.shape}")
print(f"Braki w oryginale: {maska_nan.sum()}")
print(f"Braki po FFill: {df_result['FFill'].isna().sum()}")
print(f"Braki po BFill: {df_result['BFill'].isna().sum()}")
print(f"Braki po Linear: {df_result['Linear'].isna().sum()}")

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy szereg ma 20 dni: {len(df) == 20}")
print(f"Czy indeks jest czasowy: {isinstance(df.index, pd.DatetimeIndex)}")
print(f"Czy daty sa unikalne: {df.index.is_unique}")
print(f"Czy daty sa uporzadkowane: {df.index.is_monotonic_increasing}")
print(f"Czy oryginal zawiera 6 NaN: {maska_nan.sum() == 6}")
print(f"Czy wynik ma ksztalt (20, 4): {df_result.shape == (20, 4)}")
print(f"Czy FFill nie zawiera NaN: {df_result['FFill'].notna().all()}")
print(f"Czy BFill nie zawiera NaN: {df_result['BFill'].notna().all()}")
print(f"Czy Linear nie zawiera NaN: {df_result['Linear'].notna().all()}")
print(f"Czy FFill jest poprawne: {df_result['FFill'].equals(df['Oryginal'].ffill())}")
print(f"Czy BFill jest poprawne: {df_result['BFill'].equals(df['Oryginal'].bfill())}")
print(f"Czy interpolacja jest poprawna: {interpolacja_poprawna}")
print(f"Czy zachowano znane wartosci: {zachowano_wartosci}")
print(f"Czy zachowano indeks czasowy: {df_result.index.equals(df.index)}")
print(f"Czy zachowano kolumne oryginalna: {df_result['Oryginal'].equals(df['Oryginal'])}")
print(f"Czy oryginalne dane pozostaly niezmienione: {df.equals(df_original)}")
