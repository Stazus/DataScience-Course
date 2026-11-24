# Lekcja 11 - Zadanie 14: Analiza missing data patterns

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

# Boolean DataFrame - True oznacza brak danych
missing = df.isnull()

# Maski brakujacych danych
age_missing = missing["Age"]
cabin_missing = missing["Cabin"]
embarked_missing = missing["Embarked"]

print("ANALIZA MISSING DATA PATTERNS - TITANIC")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print(f"Liczba wszystkich NaN: {missing.sum().sum()}")

# Raport brakujacych danych
raport = pd.DataFrame({
    "Liczba_NaN": missing.sum(),
    "Procent_NaN": missing.mean() * 100
})

print("\nRAPORT BRAKUJACYCH DANYCH")
print("=" * 75)
print(raport.round(2).to_string())

# Tekstowa mapa brakujacych danych
print("\nTEKSTOWA MAPA BRAKUJACYCH DANYCH")
print("=" * 75)
print("Legenda: X = NaN, . = wartosc")
print("Pierwsze 30 wierszy\n")

print(f"{'ID':>4}", end=" ")

for kolumna in df.columns:
    print(f"{kolumna[:5]:>5}", end=" ")

print()

for indeks, wiersz in missing.head(30).iterrows():
    print(f"{df.loc[indeks, 'PassengerId']:>4}", end=" ")

    for wartosc in wiersz:
        symbol = "X" if wartosc else "."
        print(f"{symbol:>5}", end=" ")

    print()

# Jednoczesne wystepowanie brakow
age_cabin = (age_missing & cabin_missing).sum()
age_embarked = (age_missing & embarked_missing).sum()
cabin_embarked = (cabin_missing & embarked_missing).sum()

wszystkie_trzy = (
    age_missing & cabin_missing & embarked_missing
).sum()

print("\nWSPOLWYSTEPOWANIE BRAKUJACYCH DANYCH")
print("=" * 75)
print(f"NaN Age: {age_missing.sum()}")
print(f"NaN Cabin: {cabin_missing.sum()}")
print(f"NaN Embarked: {embarked_missing.sum()}")
print(f"NaN Age + NaN Cabin: {age_cabin}")
print(f"NaN Age + NaN Embarked: {age_embarked}")
print(f"NaN Cabin + NaN Embarked: {cabin_embarked}")
print(f"NaN we wszystkich trzech: {wszystkie_trzy}")

# Prawdopodobienstwa warunkowe
p_cabin_age_missing = (
    cabin_missing[age_missing].mean() * 100
)

p_cabin_age_known = (
    cabin_missing[~age_missing].mean() * 100
)

p_embarked_age_missing = (
    embarked_missing[age_missing].mean() * 100
)

p_embarked_age_known = (
    embarked_missing[~age_missing].mean() * 100
)

print("\nZALEZNOSCI POMIEDZY BRAKAMI")
print("=" * 75)

print(
    f"Brak Cabin przy brakujacym Age: "
    f"{p_cabin_age_missing:.2f}%"
)

print(
    f"Brak Cabin przy znanym Age: "
    f"{p_cabin_age_known:.2f}%"
)

print(
    f"Brak Embarked przy brakujacym Age: "
    f"{p_embarked_age_missing:.2f}%"
)

print(
    f"Brak Embarked przy znanym Age: "
    f"{p_embarked_age_known:.2f}%"
)

# Macierz korelacji brakujacych danych
kolumny_z_brakami = ["Age", "Cabin", "Embarked"]

korelacja = (
    missing[kolumny_z_brakami]
    .astype(int)
    .corr()
)

print("\nMACIERZ KORELACJI BRAKUJACYCH DANYCH")
print("=" * 75)
print(korelacja.round(4).to_string())

# Tabele krzyzowe
print("\nTABELA KRZYZOWA - AGE I CABIN")
print("=" * 75)

print(pd.crosstab(
    age_missing,
    cabin_missing,
    rownames=["Brak Age"],
    colnames=["Brak Cabin"],
    margins=True
).to_string())

print("\nTABELA KRZYZOWA - AGE I EMBARKED")
print("=" * 75)

print(pd.crosstab(
    age_missing,
    embarked_missing,
    rownames=["Brak Age"],
    colnames=["Brak Embarked"],
    margins=True
).to_string())

# Podzial pasazerow wedlug dostepnosci wieku
df_age_missing = df[age_missing]
df_age_known = df[~age_missing]

# Wskazniki przezycia
survival_missing = df_age_missing["Survived"].mean() * 100
survival_known = df_age_known["Survived"].mean() * 100

roznica = survival_known - survival_missing

# Tabela porownawcza
survival_stats = pd.DataFrame({
    "Grupa": ["Brak wieku", "Znany wiek"],
    "Pasazerowie": [
        len(df_age_missing),
        len(df_age_known)
    ],
    "Ocalali": [
        df_age_missing["Survived"].sum(),
        df_age_known["Survived"].sum()
    ],
    "Przezywalnosc_%": [
        survival_missing,
        survival_known
    ]
})

print("\nPRZEZYWALNOSC A BRAKUJACY WIEK")
print("=" * 75)
print(survival_stats.round(2).to_string(index=False))

print(f"\nRoznica przezywalnosci: {roznica:.2f} p.p.")

# Tekstowa wizualizacja
print("\nTEKSTOWY WYKRES PRZEZYWALNOSCI")
print("=" * 75)
print("Legenda: jeden znak = okolo 2%")

for grupa, procent in zip(
    survival_stats["Grupa"],
    survival_stats["Przezywalnosc_%"]
):
    slupek = "█" * round(procent / 2)
    print(f"{grupa:<15} | {slupek:<50} {procent:.2f}%")

# Wnioski
print("\nWNIOSKI")
print("=" * 75)

print(
    "1. Najwiecej brakujacych danych wystepuje "
    f"w kolumnie {raport['Liczba_NaN'].idxmax()}."
)

print(
    f"2. Jednoczesny brak Age i Cabin dotyczy "
    f"{age_cabin} pasazerow."
)

print(
    f"3. Korelacja brakow Age i Cabin: "
    f"{korelacja.loc['Age', 'Cabin']:.4f}."
)

print(
    f"4. Korelacja brakow Age i Embarked: "
    f"{korelacja.loc['Age', 'Embarked']:.4f}."
)

if survival_known > survival_missing:
    print(
        "5. Pasazerowie ze znanym wiekiem mieli "
        "wyzszy wskaznik przezycia."
    )
elif survival_known < survival_missing:
    print(
        "5. Pasazerowie bez znanego wieku mieli "
        "wyzszy wskaznik przezycia."
    )
else:
    print("5. Obie grupy mialy identyczna przezywalnosc.")

print(
    "6. Zaobserwowane zaleznosci nie dowodza "
    "zwiazku przyczynowego."
)

print(
    "7. Sama analiza nie pozwala jednoznacznie "
    "ustalic mechanizmu brakujacych danych."
)

# Podsumowanie
print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Liczba pasazerow: {len(df)}")
print(f"Kolumny z brakami: {missing.any().sum()}")
print(f"Laczna liczba NaN: {missing.sum().sum()}")
print(f"Pasazerowie bez wieku: {len(df_age_missing)}")
print(f"Pasazerowie ze znanym wiekiem: {len(df_age_known)}")
print(f"Przezywalnosc bez wieku: {survival_missing:.2f}%")
print(f"Przezywalnosc ze znanym wiekiem: {survival_known:.2f}%")

# Weryfikacja
print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy dataset ma 891 wierszy: {len(df) == 891}")
print(f"Czy dataset ma 12 kolumn: {len(df.columns) == 12}")
print(f"Czy maska ma poprawny ksztalt: {missing.shape == df.shape}")
print(f"Czy maska zawiera typ bool: {(missing.dtypes == bool).all()}")
print(f"Czy Age ma 177 brakow: {age_missing.sum() == 177}")
print(f"Czy Cabin ma 687 brakow: {cabin_missing.sum() == 687}")
print(f"Czy Embarked ma 2 braki: {embarked_missing.sum() == 2}")
print(f"Czy lacznie jest 866 NaN: {missing.sum().sum() == 866}")
print(f"Czy mapa obejmuje 30 wierszy: {len(missing.head(30)) == 30}")
print(f"Czy wspolne braki Age i Cabin sa poprawne: {age_cabin == missing.loc[age_missing, 'Cabin'].sum()}")
print(f"Czy wspolne braki Age i Embarked sa poprawne: {age_embarked == missing.loc[age_missing, 'Embarked'].sum()}")
print(f"Czy macierz korelacji ma ksztalt (3, 3): {korelacja.shape == (3, 3)}")
print(f"Czy macierz korelacji jest symetryczna: {np.allclose(korelacja, korelacja.T)}")
print(f"Czy przekatna korelacji zawiera jedynki: {np.allclose(np.diag(korelacja), 1)}")
print(f"Czy podzial obejmuje wszystkich pasazerow: {len(df_age_missing) + len(df_age_known) == len(df)}")
print(f"Czy zachowano liczbe ocalalych: {survival_stats['Ocalali'].sum() == df['Survived'].sum()}")
print(f"Czy wskazniki przezycia sa poprawne: {survival_stats['Przezywalnosc_%'].between(0, 100).all()}")
print(f"Czy oryginalne dane pozostaly niezmienione: {df.equals(df_original)}")
