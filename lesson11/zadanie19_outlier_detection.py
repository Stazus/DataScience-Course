# Lekcja 11 - Zadanie 19: Outlier detection i obsluga

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

# Obliczenie kwartyli
q1 = df["Fare"].quantile(0.25)
q3 = df["Fare"].quantile(0.75)

# Rozstep miedzykwartylowy
iqr = q3 - q1

# Granice IQR
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Maska wartosci odstajacych
outlier_mask = (
    (df["Fare"] < lower_bound)
    | (df["Fare"] > upper_bound)
)

# DataFrame zawierajacy outliers
outliers = df.loc[outlier_mask].copy()

print("OUTLIER DETECTION - DATASET TITANIC")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)

print(f"Shape: {df.shape}")
print(f"Liczba pasazerow: {len(df)}")
print(f"Brakujace Fare: {df['Fare'].isna().sum()}")

print("\nSTATYSTYKI FARE PRZED TRANSFORMACJA")
print("=" * 75)

print(df["Fare"].describe().round(4))

print("\nDETEKCJA OUTLIERS METODA IQR")
print("=" * 75)

print(f"Q1: {q1:.4f}")
print(f"Q3: {q3:.4f}")
print(f"IQR: {iqr:.4f}")
print(f"Dolna granica: {lower_bound:.4f}")
print(f"Gorna granica: {upper_bound:.4f}")

print(
    f"Zakres typowych wartosci: "
    f"[{lower_bound:.4f}, {upper_bound:.4f}]"
)

print(f"Liczba outliers: {len(outliers)}")

print(
    f"Procent outliers: "
    f"{len(outliers) / len(df) * 100:.2f}%"
)

print(
    f"Outliers ponizej dolnej granicy: "
    f"{(df['Fare'] < lower_bound).sum()}"
)

print(
    f"Outliers powyzej gornej granicy: "
    f"{(df['Fare'] > upper_bound).sum()}"
)

print("\nTOP 10 NAJWYZSZYCH WARTOSCI ODSTAJACYCH")
print("=" * 75)

print(
    outliers[
        ["PassengerId", "Name", "Pclass", "Fare"]
    ]
    .sort_values("Fare", ascending=False)
    .head(10)
    .to_string(index=False)
)

# STRATEGIA 1 - usuwanie outliers
df_removed = df.loc[~outlier_mask].copy()

# STRATEGIA 2 - capping
df_capped = df.copy()

df_capped["Fare"] = np.clip(
    df_capped["Fare"],
    lower_bound,
    upper_bound
)

# STRATEGIA 3 - transformacja logarytmiczna
df_log = df.copy()

df_log["Fare"] = np.log1p(df_log["Fare"])

print("\nSTRATEGIA 1 - USUWANIE OUTLIERS")
print("=" * 75)

print(f"Shape przed: {df.shape}")
print(f"Shape po: {df_removed.shape}")
print(f"Usuniete wiersze: {len(df) - len(df_removed)}")

print("\nStatystyki Fare:")
print(df_removed["Fare"].describe().round(4))

print("\nSTRATEGIA 2 - CAPPING")
print("=" * 75)

print(f"Shape przed: {df.shape}")
print(f"Shape po: {df_capped.shape}")

print(
    f"Zmienione wartosci: "
    f"{(df_capped['Fare'] != df['Fare']).sum()}"
)

print("\nStatystyki Fare:")
print(df_capped["Fare"].describe().round(4))

print("\nSTRATEGIA 3 - TRANSFORMACJA LOGARYTMICZNA")
print("=" * 75)

print(f"Shape przed: {df.shape}")
print(f"Shape po: {df_log.shape}")

print("\nStatystyki Fare po log1p:")
print(df_log["Fare"].describe().round(4))

# Porownanie statystyk wszystkich strategii
comparison = pd.DataFrame({
    "Oryginal": df["Fare"].describe(),
    "Usuwanie": df_removed["Fare"].describe(),
    "Capping": df_capped["Fare"].describe(),
    "Log1p": df_log["Fare"].describe()
})

print("\nPOROWNANIE STATYSTYK")
print("=" * 75)

print(comparison.round(4).to_string())

print(
    "\nUwaga: Log1p przedstawia wartosci "
    "w skali logarytmicznej, a nie ceny biletow."
)

# Analiza skosnosci rozkladow
skewness = pd.Series({
    "Oryginal": df["Fare"].skew(),
    "Usuwanie": df_removed["Fare"].skew(),
    "Capping": df_capped["Fare"].skew(),
    "Log1p": df_log["Fare"].skew()
})

skewness_report = pd.DataFrame({
    "Skosnosc": skewness,
    "Skosnosc_abs": skewness.abs()
})

print("\nPOROWNANIE SKOSNOSCI ROZKLADOW")
print("=" * 75)

print(skewness_report.round(4).to_string())

# Najmniejsza bezwzgledna skosnosc
best_strategy = skewness.drop("Oryginal").abs().idxmin()

print(f"\nNajbardziej symetryczny rozklad: {best_strategy}")

print(
    f"Skosnosc najlepszej strategii: "
    f"{skewness[best_strategy]:.4f}"
)

# Tekstowy wykres bezwzglednej skosnosci
print("\nTEKSTOWY WYKRES SKOSNOSCI")
print("=" * 75)

print("Legenda: jeden znak = okolo 0.1 skosnosci")
print("Krotszy slupek oznacza mniejsza asymetrie.")

for name, value in skewness.items():
    bar = "█" * round(abs(value) * 10)

    print(
        f"{name:<12} | "
        f"{bar:<55} {value:.4f}"
    )

# Porownanie zachowanych rekordow
datasets = {
    "Oryginal": df,
    "Usuwanie": df_removed,
    "Capping": df_capped,
    "Log1p": df_log
}

records_report = pd.DataFrame([
    {
        "Strategia": name,
        "Wiersze": len(data),
        "Usuniete": len(df) - len(data),
        "Zachowane_%": len(data) / len(df) * 100
    }
    for name, data in datasets.items()
])

print("\nPOROWNANIE ZACHOWANYCH REKORDOW")
print("=" * 75)

print(records_report.round(2).to_string(index=False))

# Sprawdzenie pozostalych outliers wedlug
# pierwotnych granic IQR
removed_outliers = (
    (df_removed["Fare"] < lower_bound)
    | (df_removed["Fare"] > upper_bound)
).sum()

capped_outliers = (
    (df_capped["Fare"] < lower_bound)
    | (df_capped["Fare"] > upper_bound)
).sum()

print("\nOUTLIERS PO ZASTOSOWANIU STRATEGII")
print("=" * 75)

print(f"Oryginal: {len(outliers)}")
print(f"Usuwanie: {removed_outliers}")
print(f"Capping: {capped_outliers}")

print(
    "Log1p: pierwotne granice IQR nie maja "
    "zastosowania do skali logarytmicznej."
)

# Ponowna detekcja IQR w skali logarytmicznej
log_q1 = df_log["Fare"].quantile(0.25)
log_q3 = df_log["Fare"].quantile(0.75)
log_iqr = log_q3 - log_q1

log_lower = log_q1 - 1.5 * log_iqr
log_upper = log_q3 + 1.5 * log_iqr

log_outliers = (
    (df_log["Fare"] < log_lower)
    | (df_log["Fare"] > log_upper)
).sum()

print("\nDETEKCJA IQR PO LOG1P")
print("=" * 75)

print(f"Dolna granica: {log_lower:.4f}")
print(f"Gorna granica: {log_upper:.4f}")
print(f"Liczba outliers w skali log: {log_outliers}")

print("\nWNIOSKI")
print("=" * 75)

print(
    "1. Metoda IQR pozwala wykryc "
    "potencjalne wartosci odstajace."
)

print(
    "2. Usuwanie outliers zmniejsza "
    "liczbe rekordow."
)

print(
    "3. Capping zachowuje wszystkie rekordy, "
    "ale ogranicza skrajne wartosci."
)

print(
    "4. Log1p zachowuje wszystkie rekordy "
    "i zmienia skale danych."
)

print(
    f"5. Najmniejsza bezwzgledna skosnosc "
    f"uzyskano dla strategii {best_strategy}."
)

print(
    "6. Wysoka cena biletu nie musi "
    "oznaczac bledu danych."
)

print(
    "7. Wybor strategii zalezy od celu analizy "
    "i wymagan modelu ML."
)

print(
    "8. Transformacja logarytmiczna nie gwarantuje "
    "usuniecia wszystkich outliers."
)

print("\nPODSUMOWANIE")
print("=" * 75)

print(f"Liczba pasazerow: {len(df)}")
print(f"Liczba outliers: {len(outliers)}")
print(f"Zakres IQR: [{lower_bound:.4f}, {upper_bound:.4f}]")
print(f"Shape po usuwaniu: {df_removed.shape}")
print(f"Shape po cappingu: {df_capped.shape}")
print(f"Shape po log1p: {df_log.shape}")
print(f"Najlepsza strategia wedlug skosnosci: {best_strategy}")

# Weryfikacja poprawnosci
tests = {
    "Dataset ma 891 wierszy":
        len(df) == 891,

    "Dataset ma 12 kolumn":
        len(df.columns) == 12,

    "Fare nie zawiera NaN":
        df["Fare"].notna().all(),

    "IQR jest dodatni":
        iqr > 0,

    "Granice IQR sa poprawne":
        lower_bound < upper_bound,

    "Wykryto 116 outliers":
        len(outliers) == 116,

    "Usuwanie zachowalo 775 wierszy":
        len(df_removed) == 775,

    "Usunieto wszystkie wykryte outliers":
        removed_outliers == 0,

    "Capping zachowal wszystkie wiersze":
        len(df_capped) == len(df),

    "Capping ograniczyl wszystkie outliers":
        capped_outliers == 0,

    "Capping zmienil tylko outliers":
        (df_capped["Fare"] != df["Fare"]).equals(
            outlier_mask
        ),

    "Log1p zachowal wszystkie wiersze":
        len(df_log) == len(df),

    "Transformacja log1p jest poprawna":
        np.allclose(
            df_log["Fare"],
            np.log1p(df["Fare"])
        ),

    "Transformacja log1p jest odwracalna":
        np.allclose(
            np.expm1(df_log["Fare"]),
            df["Fare"]
        ),

    "Wartosci log1p sa skonczone":
        np.isfinite(df_log["Fare"]).all(),

    "Pozostale kolumny po usuwaniu sa niezmienione":
        df_removed.drop(columns="Fare").equals(
            df.loc[~outlier_mask].drop(columns="Fare")
        ),

    "Pozostale kolumny po cappingu sa niezmienione":
        df_capped.drop(columns="Fare").equals(
            df.drop(columns="Fare")
        ),

    "Pozostale kolumny po log1p sa niezmienione":
        df_log.drop(columns="Fare").equals(
            df.drop(columns="Fare")
        ),

    "Obliczono skosnosc wszystkich strategii":
        len(skewness) == 4,

    "Najlepsza strategia ma najmniejsza skosnosc":
        np.isclose(
            abs(skewness[best_strategy]),
            skewness.drop("Oryginal").abs().min()
        ),

    "Oryginalne dane pozostaly niezmienione":
        df.equals(df_original)
}

print("\nWERYFIKACJA")
print("=" * 75)

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())

print(f"\nZaliczone testy: {passed}/{len(tests)}")

if all(tests.values()):
    print("Wszystkie testy zakonczone pomyslnie.")
else:
    print("Nie wszystkie testy zostaly zaliczone.")
