# Lekcja 11 - Zadanie 17: Korelacja miedzy brakami danych

import pandas as pd
import numpy as np
from itertools import combinations


# Adres URL datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# Wczytanie danych
df = pd.read_csv(url)

# Kopia oryginalnych danych
df_original = df.copy()

# Boolean DataFrame
# True - brak danych
# False - wartosc istnieje
missing = df.isnull()

# Pelna macierz korelacji brakujacych danych
matrix = missing.corr()

# Kolumny zawierajace braki
missing_columns = missing.columns[missing.any()].tolist()

# Macierz korelacji kolumn z brakami
matrix_missing = matrix.loc[
    missing_columns, missing_columns
]

print("KORELACJA MIEDZY BRAKAMI DANYCH - TITANIC")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print(f"Liczba wszystkich NaN: {missing.sum().sum()}")

print("\nBOOLEAN DATAFRAME - PIERWSZE 10 WIERSZY")
print("=" * 75)
print(missing.head(10).to_string())

print("\nRAPORT BRAKUJACYCH DANYCH")
print("=" * 75)

report = pd.DataFrame({
    "Liczba_NaN": missing.sum(),
    "Procent_NaN": missing.mean() * 100
})

print(report.round(2).to_string())

print("\nPELNA MACIERZ KORELACJI")
print("=" * 75)

# Wymaganie zadania
print(matrix.round(2))

print("\nMACIERZ KORELACJI KOLUMN Z BRAKAMI")
print("=" * 75)
print(matrix_missing.round(4))

print("\nINTERPRETACJA WSPOLCZYNNIKA KORELACJI")
print("=" * 75)
print("r = 1  : idealna dodatnia korelacja")
print("r = 0  : brak korelacji liniowej")
print("r = -1 : idealna ujemna korelacja")
print("NaN    : korelacja niezdefiniowana")


# Funkcja interpretujaca sile korelacji
def interpret_correlation(r):
    if pd.isna(r):
        return "niezdefiniowana"

    strength = abs(r)

    if strength < 0.1:
        return "znikoma"
    elif strength < 0.3:
        return "slaba"
    elif strength < 0.5:
        return "umiarkowana"
    elif strength < 0.7:
        return "silna"
    else:
        return "bardzo silna"


# Analiza wszystkich par kolumn z brakami
pairs = []

for col1, col2 in combinations(missing_columns, 2):
    r = matrix.loc[col1, col2]

    common_missing = (
        missing[col1] & missing[col2]
    ).sum()

    if r > 0:
        direction = "dodatnia"
    elif r < 0:
        direction = "ujemna"
    else:
        direction = "brak"

    pairs.append({
        "Kolumna_1": col1,
        "Kolumna_2": col2,
        "Korelacja": r,
        "Wspolne_NaN": common_missing,
        "Kierunek": direction,
        "Sila": interpret_correlation(r)
    })

df_pairs = pd.DataFrame(pairs)

print("\nANALIZA PAR KOLUMN")
print("=" * 75)
print(df_pairs.round(4).to_string(index=False))

# Prawdopodobienstwa warunkowe
conditional_results = []

for col1, col2 in combinations(missing_columns, 2):

    for source, target in [(col1, col2), (col2, col1)]:

        probability_missing = (
            missing.loc[missing[source], target].mean()
            * 100
        )

        probability_present = (
            missing.loc[~missing[source], target].mean()
            * 100
        )

        conditional_results.append({
            "Warunek": source,
            "Badana_kolumna": target,
            "Przy_NaN_%": probability_missing,
            "Przy_not_NaN_%": probability_present,
            "Roznica_pp": (
                probability_missing - probability_present
            )
        })

df_conditional = pd.DataFrame(conditional_results)

print("\nPRAWDOPODOBIENSTWA WARUNKOWE")
print("=" * 75)
print(df_conditional.round(2).to_string(index=False))

print("\nINTERPRETACJA ZALEZNOSCI")
print("=" * 75)

for _, row in df_conditional.iterrows():

    print(
        f"\nBrak {row['Warunek']} "
        f"a brak {row['Badana_kolumna']}:"
    )

    print(f"  Przy NaN: {row['Przy_NaN_%']:.2f}%")
    print(f"  Przy not NaN: {row['Przy_not_NaN_%']:.2f}%")
    print(f"  Roznica: {row['Roznica_pp']:.2f} p.p.")

    if row["Roznica_pp"] > 0:
        print("  Wniosek: wieksza obserwowana czestosc brakow.")
    elif row["Roznica_pp"] < 0:
        print("  Wniosek: mniejsza obserwowana czestosc brakow.")
    else:
        print("  Wniosek: brak roznicy.")

# Kolumny bez brakujacych danych
complete_columns = missing.columns[
    ~missing.any()
].tolist()

print("\nKOLUMNY BEZ BRAKUJACYCH DANYCH")
print("=" * 75)

for column in complete_columns:
    print(column)

print("\nDLACZEGO MACIERZ ZAWIERA NaN?")
print("=" * 75)
print("Kolumny bez brakow zawieraja wylacznie False.")
print("Ich wariancja wynosi zero.")
print("Korelacja Pearsona jest wtedy niezdefiniowana.")
print("Nie jest to blad programu.")

# Najsilniejsza korelacja poza przekatna
strongest_index = df_pairs["Korelacja"].abs().idxmax()
strongest = df_pairs.loc[strongest_index]

print("\nNAJSILNIEJSZA ZAOBSERWOWANA KORELACJA")
print("=" * 75)
print(f"Kolumna 1: {strongest['Kolumna_1']}")
print(f"Kolumna 2: {strongest['Kolumna_2']}")
print(f"Korelacja: {strongest['Korelacja']:.4f}")
print(f"Sila: {strongest['Sila']}")
print(f"Kierunek: {strongest['Kierunek']}")

print("\nWNIOSKI")
print("=" * 75)
print("1. Braki wystepuja w Age, Cabin i Embarked.")
print("2. Braki Age i Cabin wykazuja slaba dodatnia korelacje.")
print("3. Pozostale korelacje maja bardzo mala wartosc bezwzgledna.")
print("4. Brak Age wiaze sie z czestszym brakiem Cabin.")
print("5. Korelacja nie dowodzi zwiazku przyczynowego.")
print("6. Sama korelacja nie okresla mechanizmu brakow danych.")
print("7. Dwa braki Embarked ograniczaja wiarygodnosc wnioskow.")

print("\nPODSUMOWANIE")
print("=" * 75)
print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print(f"Shape macierzy: {matrix.shape}")
print(f"Kolumny z brakami: {len(missing_columns)}")
print(f"Kolumny bez brakow: {len(complete_columns)}")
print(f"Liczba analizowanych par: {len(df_pairs)}")
print(f"Laczna liczba NaN: {missing.sum().sum()}")

print("\nWERYFIKACJA")
print("=" * 75)
print(f"Czy dataset ma 891 wierszy: {len(df) == 891}")
print(f"Czy dataset ma 12 kolumn: {len(df.columns) == 12}")
print(f"Czy maska ma poprawny ksztalt: {missing.shape == df.shape}")
print(f"Czy maska zawiera typ bool: {(missing.dtypes == bool).all()}")
print(f"Czy lacznie jest 866 NaN: {missing.sum().sum() == 866}")
print(f"Czy macierz ma ksztalt (12, 12): {matrix.shape == (12, 12)}")
print(f"Czy macierz jest symetryczna: {np.allclose(matrix, matrix.T, equal_nan=True)}")
print(f"Czy 3 kolumny maja braki: {len(missing_columns) == 3}")
print(f"Czy 9 kolumn nie ma brakow: {len(complete_columns) == 9}")
print(f"Czy macierz brakow ma ksztalt (3, 3): {matrix_missing.shape == (3, 3)}")
print(f"Czy przekatna zawiera jedynki: {np.allclose(np.diag(matrix_missing), 1)}")
print(f"Czy korelacje sa w zakresie -1 do 1: {df_pairs['Korelacja'].between(-1, 1).all()}")
print(f"Czy korelacja Age-Cabin jest poprawna: {np.isclose(matrix.loc['Age', 'Cabin'], 0.1441, atol=0.0001)}")
print(f"Czy przeanalizowano 3 pary: {len(df_pairs) == 3}")
print(f"Czy obliczono 6 zaleznosci warunkowych: {len(df_conditional) == 6}")
print(f"Czy korelacje stalych kolumn sa NaN: {matrix.loc[complete_columns].isna().all().all()}")
print(f"Czy oryginalne dane pozostaly niezmienione: {df.equals(df_original)}")
