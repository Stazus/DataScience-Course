# Lekcja 11 - Zadanie 12: Optymalizacja typow danych

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

# DataFrame przeznaczony do optymalizacji
df_optimized = df.copy()

# Zuzycie pamieci przed optymalizacja
pamiec_przed = df.memory_usage(deep=True).sum()

# Kolumny przeznaczone do konwersji
kolumny_int8 = ["Pclass", "Survived", "SibSp", "Parch"]
kolumny_category = ["Sex", "Embarked"]

print("OPTYMALIZACJA TYPOW DANYCH - TITANIC")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba wierszy: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")

print("\nTYPY DANYCH PRZED OPTYMALIZACJA")
print("=" * 75)
print(df.dtypes.to_string())

# Sprawdzenie zakresu typu int8
zakres_int8 = np.iinfo(np.int8)

print("\nSPRAWDZENIE ZAKRESU INT8")
print("=" * 75)
print(f"Zakres int8: {zakres_int8.min} do {zakres_int8.max}")

for kolumna in kolumny_int8:
    minimum = df[kolumna].min()
    maksimum = df[kolumna].max()

    bezpieczna = (
        df[kolumna].notna().all()
        and minimum >= zakres_int8.min
        and maksimum <= zakres_int8.max
    )

    print(
        f"{kolumna:12} | min: {minimum:3} | "
        f"max: {maksimum:3} | bezpieczna: {bezpieczna}"
    )

    if not bezpieczna:
        raise ValueError(f"Niebezpieczna konwersja: {kolumna}")

# Konwersja kolumn liczbowych na int8
df_optimized[kolumny_int8] = (
    df_optimized[kolumny_int8].astype("int8")
)

# Konwersja kolumn tekstowych na category
df_optimized[kolumny_category] = (
    df_optimized[kolumny_category].astype("category")
)

print("\nTYPY DANYCH PO OPTYMALIZACJI")
print("=" * 75)
print(df_optimized.dtypes.to_string())

# Zuzycie pamieci po optymalizacji
pamiec_po = df_optimized.memory_usage(deep=True).sum()

# Obliczenie oszczednosci
oszczednosc = pamiec_przed - pamiec_po
redukcja = oszczednosc / pamiec_przed * 100

# Porownanie typow danych
raport_typow = pd.DataFrame({
    "Typ_przed": df.dtypes.astype(str),
    "Typ_po": df_optimized.dtypes.astype(str)
})

print("\nPOROWNANIE TYPOW DANYCH")
print("=" * 75)
print(raport_typow.to_string())

# Zuzycie pamieci dla poszczegolnych kolumn
raport_pamieci = pd.DataFrame({
    "Przed_B": df.memory_usage(deep=True),
    "Po_B": df_optimized.memory_usage(deep=True)
})

raport_pamieci["Oszczednosc_B"] = (
    raport_pamieci["Przed_B"] - raport_pamieci["Po_B"]
)

raport_pamieci["Redukcja_%"] = (
    raport_pamieci["Oszczednosc_B"]
    / raport_pamieci["Przed_B"] * 100
)

print("\nZUZYCIE PAMIECI WEDLUG KOLUMN")
print("=" * 75)
print(raport_pamieci.round(2).to_string())

print("\nKATEGORIE")
print("=" * 75)

for kolumna in kolumny_category:
    print(f"\nKolumna: {kolumna}")
    print(f"Kategorie: {df_optimized[kolumna].cat.categories.tolist()}")
    print(df_optimized[kolumna].value_counts(dropna=False).to_string())

print("\nZUZYCIE PAMIECI PRZED I PO")
print("=" * 75)
print(f"Przed: {pamiec_przed} B ({pamiec_przed / 1024:.2f} KiB)")
print(f"Po: {pamiec_po} B ({pamiec_po / 1024:.2f} KiB)")
print(f"Oszczednosc: {oszczednosc} B ({oszczednosc / 1024:.2f} KiB)")
print(f"Redukcja pamieci: {redukcja:.2f}%")

# Tekstowy wykres zuzycia pamieci
print("\nTEKSTOWY WYKRES ZUZYCIA PAMIECI")
print("=" * 75)

for etykieta, wartosc in [
    ("Przed", pamiec_przed),
    ("Po", pamiec_po)
]:
    dlugosc = round(wartosc / pamiec_przed * 50)
    slupek = "█" * dlugosc

    print(
        f"{etykieta:6} | {slupek:50} "
        f"{wartosc / 1024:.2f} KiB"
    )

# Przywrocenie typow do porownania wartosci
df_restored = df_optimized.astype(df.dtypes.to_dict())

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Shape przed: {df.shape}")
print(f"Shape po: {df_optimized.shape}")
print(f"Zoptymalizowane kolumny: {len(kolumny_int8 + kolumny_category)}")
print(f"Redukcja pamieci: {redukcja:.2f}%")
print(f"NaN przed: {df.isna().sum().sum()}")
print(f"NaN po: {df_optimized.isna().sum().sum()}")

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy dataset ma 891 wierszy: {len(df) == 891}")
print(f"Czy dataset ma 12 kolumn: {len(df.columns) == 12}")

for kolumna in kolumny_int8:
    print(
        f"Czy {kolumna} ma typ int8: "
        f"{str(df_optimized[kolumna].dtype) == 'int8'}"
    )

for kolumna in kolumny_category:
    print(
        f"Czy {kolumna} ma typ category: "
        f"{str(df_optimized[kolumna].dtype) == 'category'}"
    )

print(f"Czy zmniejszono zuzycie pamieci: {pamiec_po < pamiec_przed}")
print(f"Czy redukcja jest poprawna: {0 < redukcja <= 100}")
print(f"Czy zachowano ksztalt DataFrame: {df.shape == df_optimized.shape}")
print(f"Czy zachowano nazwy kolumn: {df.columns.equals(df_optimized.columns)}")
print(f"Czy zachowano indeksy: {df.index.equals(df_optimized.index)}")
print(f"Czy zachowano wszystkie NaN: {df.isna().equals(df_optimized.isna())}")
print(f"Czy zachowano wszystkie wartosci: {df_restored.equals(df)}")
print(f"Czy oryginalne dane pozostaly niezmienione: {df.equals(df_original)}")
