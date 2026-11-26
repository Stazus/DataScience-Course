# Lekcja 12 - Zadanie 19: Multi-Dataset Aggregation

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


def survival_bar(rate):
    """Jeden znak odpowiada okolo 2 procentom."""
    return "█" * int(round(rate / 2))


# =========================================================
# 1. WCZYTANIE DATASETU TITANIC
# =========================================================

url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

titanic = pd.read_csv(url)

titanic_original = titanic.copy(deep=True)

print("=" * 75)
print("MULTI-DATASET AGGREGATION - TITANIC")
print("=" * 75)


section("DANE WEJSCIOWE - TITANIC")

print(f"Shape: {titanic.shape}")
print(f"Liczba pasazerow: {len(titanic)}")
print(f"Liczba kolumn: {len(titanic.columns)}")

print(
    "Brakujace Embarked:",
    titanic["Embarked"].isna().sum()
)

print(
    "Brakujace Age:",
    titanic["Age"].isna().sum()
)


section("PIERWSZE 10 REKORDOW")

print(
    titanic[
        [
            "PassengerId",
            "Pclass",
            "Sex",
            "Age",
            "Fare",
            "Embarked",
            "Survived"
        ]
    ].head(10).to_string(index=False)
)


section("ROZKLAD PORTOW PRZED POLACZENIEM")

print(
    titanic["Embarked"]
    .value_counts(dropna=False)
    .to_string()
)


# =========================================================
# 2. POMOCNICZY DATAFRAME Z PORTAMI
# =========================================================

ports = pd.DataFrame({
    "Embarked": ["S", "C", "Q"],
    "Port_Name": [
        "Southampton",
        "Cherbourg",
        "Queenstown"
    ],
    "Country": ["UK", "France", "Ireland"],
    "Port_Size": ["Large", "Medium", "Small"]
})

ports_original = ports.copy(deep=True)


section("POMOCNICZY DATAFRAME - PORTS")

print(ports.to_string(index=False))

print(f"\nShape: {ports.shape}")
print(f"Liczba portow: {len(ports)}")

print(
    "Unikalne klucze Embarked:",
    ports["Embarked"].is_unique
)


# =========================================================
# 3. LACZENIE DATASETOW
# =========================================================

merged = pd.merge(
    titanic,
    ports,
    on="Embarked",
    how="left",
    validate="many_to_one",
    indicator=True
)


section("WYNIK POLACZENIA DATASETOW")

print(f"Shape Titanic: {titanic.shape}")
print(f"Shape Ports: {ports.shape}")
print(f"Shape po merge: {merged.shape}")

print("\nStatus dopasowania rekordow:")

print(
    merged["_merge"]
    .value_counts()
    .to_string()
)


# Rekordy bez dopasowania
unmatched = merged[
    merged["_merge"] == "left_only"
].copy()


section("REKORDY BEZ DOPASOWANIA")

print(f"Liczba niedopasowanych: {len(unmatched)}")

print(
    unmatched[
        [
            "PassengerId",
            "Name",
            "Embarked",
            "Port_Name",
            "Country",
            "Port_Size"
        ]
    ].to_string(index=False)
)

# Usuniecie technicznej kolumny merge
merged = merged.drop(columns="_merge")


section("STRUKTURA PO POLACZENIU")

print(f"Shape przed: {titanic.shape}")
print(f"Shape po: {merged.shape}")

new_columns = merged.columns.difference(
    titanic.columns
).tolist()

print(f"Nowe kolumny: {new_columns}")


section("PIERWSZE 10 REKORDOW PO MERGE")

print(
    merged[
        [
            "PassengerId",
            "Embarked",
            "Port_Name",
            "Country",
            "Port_Size",
            "Survived"
        ]
    ].head(10).to_string(index=False)
)


# =========================================================
# 4. ANALIZA BRAKUJACYCH DANYCH
# =========================================================

section("BRAKUJACE WARTOSCI PO MERGE")

print(
    merged[
        [
            "Embarked",
            "Port_Name",
            "Country",
            "Port_Size",
            "Age",
            "Fare"
        ]
    ].isna().sum().to_string()
)

# Dane do analizy portow
# Nie usuwamy rekordow z glownego DataFrame.
known_ports = merged[
    merged["Port_Name"].notna()
].copy()

unknown_ports = merged[
    merged["Port_Name"].isna()
].copy()

print(f"\nZnany port: {len(known_ports)}")
print(f"Nieznany port: {len(unknown_ports)}")

print(
    f"Procent nieznanych portow: "
    f"{len(unknown_ports) / len(merged) * 100:.2f}%"
)


# =========================================================
# 5. PODSTAWOWA AGREGACJA WEDLUG PORTU
# =========================================================

port_basic = known_ports.groupby(
    "Port_Name"
).agg(
    Sredni_wiek=("Age", "mean"),
    Survival_Rate=("Survived", "mean"),
    Srednia_oplata=("Fare", "mean")
)

port_basic["Survival_Rate"] *= 100


section("PODSTAWOWE STATYSTYKI WEDLUG PORTU")

print(port_basic.round(2).to_string())


# =========================================================
# 6. SZCZEGOLOWA AGREGACJA WIELOPOZIOMOWA
# =========================================================

port_stats = known_ports.groupby(
    ["Embarked", "Port_Name", "Country", "Port_Size"]
).agg(
    Liczba_pasazerow=("PassengerId", "size"),
    Znany_wiek=("Age", "count"),
    Przezyli=("Survived", "sum"),
    Sredni_wiek=("Age", "mean"),
    Mediana_wieku=("Age", "median"),
    Min_wiek=("Age", "min"),
    Max_wiek=("Age", "max"),
    Srednia_oplata=("Fare", "mean"),
    Mediana_oplaty=("Fare", "median"),
    Min_oplata=("Fare", "min"),
    Max_oplata=("Fare", "max"),
    Odchylenie_oplaty=("Fare", "std")
).reset_index()

port_stats["Nie_przezyli"] = (
    port_stats["Liczba_pasazerow"]
    - port_stats["Przezyli"]
)

port_stats["Brakujacy_wiek"] = (
    port_stats["Liczba_pasazerow"]
    - port_stats["Znany_wiek"]
)

port_stats["Survival_Rate"] = (
    port_stats["Przezyli"]
    / port_stats["Liczba_pasazerow"]
    * 100
)

port_stats["Mortality_Rate"] = (
    100 - port_stats["Survival_Rate"]
)

port_stats["Udzial_pasazerow_%"] = (
    port_stats["Liczba_pasazerow"]
    / len(known_ports)
    * 100
)


section("SZCZEGOLOWA ANALIZA PORTOW")

print(
    port_stats[
        [
            "Port_Name",
            "Country",
            "Port_Size",
            "Liczba_pasazerow",
            "Przezyli",
            "Nie_przezyli",
            "Survival_Rate",
            "Sredni_wiek",
            "Srednia_oplata"
        ]
    ].round(2).to_string(index=False)
)


section("STATYSTYKI WIEKU WEDLUG PORTU")

print(
    port_stats[
        [
            "Port_Name",
            "Znany_wiek",
            "Brakujacy_wiek",
            "Sredni_wiek",
            "Mediana_wieku",
            "Min_wiek",
            "Max_wiek"
        ]
    ].round(2).to_string(index=False)
)


section("STATYSTYKI OPLAT WEDLUG PORTU")

print(
    port_stats[
        [
            "Port_Name",
            "Srednia_oplata",
            "Mediana_oplaty",
            "Min_oplata",
            "Max_oplata",
            "Odchylenie_oplaty"
        ]
    ].round(2).to_string(index=False)
)


# =========================================================
# 7. ANALIZA WEDLUG ROZMIARU PORTU
# =========================================================

size_stats = known_ports.groupby(
    "Port_Size"
).agg(
    Liczba_portow=("Port_Name", "nunique"),
    Liczba_pasazerow=("PassengerId", "size"),
    Przezyli=("Survived", "sum"),
    Survival_Rate=("Survived", "mean"),
    Sredni_wiek=("Age", "mean"),
    Srednia_oplata=("Fare", "mean")
)

size_stats["Survival_Rate"] *= 100

size_stats = size_stats.reindex(
    ["Small", "Medium", "Large"]
)


section("ANALIZA WEDLUG ROZMIARU PORTU")

print(size_stats.round(2).to_string())


section("TEKSTOWY WYKRES PRZEZYWALNOSCI - ROZMIAR PORTU")

print("Legenda: jeden znak = okolo 2%")

for size, row in size_stats.iterrows():
    rate = row["Survival_Rate"]

    print(
        f"{size:8} | "
        f"{survival_bar(rate):50} "
        f"{rate:6.2f}%"
    )


# =========================================================
# 8. ANALIZA WEDLUG KRAJU PORTU
# =========================================================

country_stats = known_ports.groupby(
    "Country"
).agg(
    Liczba_pasazerow=("PassengerId", "size"),
    Przezyli=("Survived", "sum"),
    Survival_Rate=("Survived", "mean"),
    Sredni_wiek=("Age", "mean"),
    Srednia_oplata=("Fare", "mean")
)

country_stats["Survival_Rate"] *= 100


section("ANALIZA WEDLUG KRAJU PORTU")

print(country_stats.round(2).to_string())

print(
    "\nCountry oznacza kraj portu, "
    "a nie narodowosc pasazera."
)


# =========================================================
# 9. RANKING PORTOW
# =========================================================

ranking = port_stats.sort_values(
    "Survival_Rate",
    ascending=False
).reset_index(drop=True)

ranking.insert(
    0,
    "Pozycja",
    range(1, len(ranking) + 1)
)


section("RANKING PORTOW WEDLUG PRZEZYWALNOSCI")

print(
    ranking[
        [
            "Pozycja",
            "Port_Name",
            "Port_Size",
            "Liczba_pasazerow",
            "Survival_Rate"
        ]
    ].round(2).to_string(index=False)
)


section("TEKSTOWY WYKRES PRZEZYWALNOSCI - PORTY")

print("Legenda: jeden znak = okolo 2%")

for _, row in ranking.iterrows():
    rate = row["Survival_Rate"]

    print(
        f"{row['Port_Name']:12} | "
        f"{survival_bar(rate):50} "
        f"{rate:6.2f}%"
    )


section("TEKSTOWY WYKRES LICZBY PASAZEROW")

print("Legenda: jeden znak = okolo 15 pasazerow")

for _, row in port_stats.iterrows():
    count = row["Liczba_pasazerow"]

    bar = "█" * int(round(count / 15))

    print(
        f"{row['Port_Name']:12} | "
        f"{bar:50} {count:4}"
    )


section("TEKSTOWY WYKRES SREDNIEJ OPLATY")

print("Legenda: jeden znak = okolo 2 jednostek oplaty")

for _, row in port_stats.iterrows():
    fare = row["Srednia_oplata"]

    bar = "█" * int(round(fare / 2))

    print(
        f"{row['Port_Name']:12} | "
        f"{bar:50} {fare:7.2f}"
    )


# =========================================================
# 10. ANALIZA PORTU I KLASY PASAZERA
# =========================================================

class_counts = pd.crosstab(
    known_ports["Port_Name"],
    known_ports["Pclass"]
)

class_shares = pd.crosstab(
    known_ports["Port_Name"],
    known_ports["Pclass"],
    normalize="index"
) * 100

class_survival = known_ports.pivot_table(
    index="Port_Name",
    columns="Pclass",
    values="Survived",
    aggfunc="mean"
) * 100


section("LICZBA PASAZEROW - PORT I KLASA")

print(class_counts.to_string())


section("STRUKTURA KLAS W PORTACH - PROCENTY")

print(class_shares.round(2).to_string())


section("PRZEZYWALNOSC - PORT I KLASA")

print(class_survival.round(2).to_string())


# =========================================================
# 11. ANALIZA PORTU I PLCI
# =========================================================

sex_counts = pd.crosstab(
    known_ports["Port_Name"],
    known_ports["Sex"]
)

sex_survival = known_ports.pivot_table(
    index="Port_Name",
    columns="Sex",
    values="Survived",
    aggfunc="mean"
) * 100


section("LICZBA PASAZEROW - PORT I PLEC")

print(sex_counts.to_string())


section("PRZEZYWALNOSC - PORT I PLEC")

print(sex_survival.round(2).to_string())


# =========================================================
# 12. AGREGACJA WIELOPOZIOMOWA
# =========================================================

multi_stats = known_ports.groupby(
    ["Port_Name", "Pclass", "Sex"]
).agg(
    Liczba_pasazerow=("PassengerId", "size"),
    Przezyli=("Survived", "sum"),
    Survival_Rate=("Survived", "mean"),
    Sredni_wiek=("Age", "mean"),
    Srednia_oplata=("Fare", "mean")
).reset_index()

multi_stats["Survival_Rate"] *= 100


section("AGREGACJA - PORT, KLASA I PLEC")

print(
    multi_stats.round(2).to_string(index=False)
)


# =========================================================
# 13. TABELA PRZESTAWNA - PORT I SURVIVED
# =========================================================

survival_pivot = pd.crosstab(
    known_ports["Port_Name"],
    known_ports["Survived"]
).reindex(
    columns=[0, 1],
    fill_value=0
)

survival_pivot.columns = [
    "Nie_przezyli",
    "Przezyli"
]

survival_pivot["Razem"] = (
    survival_pivot["Nie_przezyli"]
    + survival_pivot["Przezyli"]
)

survival_pivot["Survival_Rate"] = (
    survival_pivot["Przezyli"]
    / survival_pivot["Razem"]
    * 100
)


section("TABELA PRZESTAWNA - PORT I SURVIVED")

print(survival_pivot.round(2).to_string())


# =========================================================
# 14. POROWNANIE Z WYNIKAMI GLOBALNYMI
# =========================================================

global_survival = (
    merged["Survived"].mean() * 100
)

known_survival = (
    known_ports["Survived"].mean() * 100
)

unknown_survival = (
    unknown_ports["Survived"].mean() * 100
)

weighted_survival = np.average(
    port_stats["Survival_Rate"],
    weights=port_stats["Liczba_pasazerow"]
)

comparison = port_stats[
    [
        "Port_Name",
        "Port_Size",
        "Liczba_pasazerow",
        "Survival_Rate"
    ]
].copy()

comparison["Roznica_od_globalnej_pp"] = (
    comparison["Survival_Rate"]
    - global_survival
)


section("POROWNANIE Z GLOBALNA PRZEZYWALNOSCIA")

print(
    comparison.round(2).to_string(index=False)
)

print(
    f"\nGlobalna przezywalnosc: "
    f"{global_survival:.2f}%"
)

print(
    f"Przezywalnosc znanych portow: "
    f"{known_survival:.2f}%"
)

print(
    f"Przezywalnosc nieznanych portow: "
    f"{unknown_survival:.2f}%"
)

print(
    f"Srednia wazona portow: "
    f"{weighted_survival:.2f}%"
)


# =========================================================
# 15. ANALIZA NAJLEPSZYCH I NAJGORSZYCH PORTOW
# =========================================================

best_port = ranking.iloc[0]
worst_port = ranking.iloc[-1]

largest_port = port_stats.loc[
    port_stats["Liczba_pasazerow"].idxmax()
]

highest_fare = port_stats.loc[
    port_stats["Srednia_oplata"].idxmax()
]

lowest_fare = port_stats.loc[
    port_stats["Srednia_oplata"].idxmin()
]

oldest_port = port_stats.loc[
    port_stats["Sredni_wiek"].idxmax()
]

youngest_port = port_stats.loc[
    port_stats["Sredni_wiek"].idxmin()
]


section("POROWNANIE PORTOW")

print(
    f"Najwyzsza przezywalnosc: "
    f"{best_port['Port_Name']} - "
    f"{best_port['Survival_Rate']:.2f}%"
)

print(
    f"Najnizsza przezywalnosc: "
    f"{worst_port['Port_Name']} - "
    f"{worst_port['Survival_Rate']:.2f}%"
)

print(
    f"Roznica przezywalnosci: "
    f"{best_port['Survival_Rate'] - worst_port['Survival_Rate']:.2f} p.p."
)

print(
    f"Najwiecej pasazerow: "
    f"{largest_port['Port_Name']} - "
    f"{largest_port['Liczba_pasazerow']}"
)

print(
    f"Najwyzsza srednia oplata: "
    f"{highest_fare['Port_Name']} - "
    f"{highest_fare['Srednia_oplata']:.2f}"
)

print(
    f"Najnizsza srednia oplata: "
    f"{lowest_fare['Port_Name']} - "
    f"{lowest_fare['Srednia_oplata']:.2f}"
)

print(
    f"Najwyzszy sredni wiek: "
    f"{oldest_port['Port_Name']} - "
    f"{oldest_port['Sredni_wiek']:.2f}"
)

print(
    f"Najnizszy sredni wiek: "
    f"{youngest_port['Port_Name']} - "
    f"{youngest_port['Sredni_wiek']:.2f}"
)


# =========================================================
# 16. ANALIZA ROZMIARU PORTU
# =========================================================

section("CZY ROZMIAR PORTU MA ZWIAZEK Z PRZEZYCIEM?")

for size, row in size_stats.iterrows():
    print(
        f"{size:8}: "
        f"{row['Survival_Rate']:.2f}%"
    )

rates = size_stats["Survival_Rate"]

if rates.is_monotonic_increasing:
    print("\nPrzezywalnosc rosnie wraz z rozmiarem portu.")

elif rates.is_monotonic_decreasing:
    print("\nPrzezywalnosc maleje wraz z rozmiarem portu.")

else:
    print(
        "\nBrak monotonicznej zaleznosci "
        "miedzy rozmiarem portu a przezywalnoscia."
    )

print(
    "Kazda kategoria rozmiaru zawiera tylko jeden port."
)

print(
    "Nie mozna oddzielic efektu rozmiaru "
    "od innych cech konkretnego portu."
)

print(
    "Klasa biletu, plec i wiek moga "
    "wspolwyjasniac obserwowane roznice."
)


# =========================================================
# 17. ANALIZA ZUZYCIA PAMIECI
# =========================================================

memory_before = (
    titanic.memory_usage(deep=True).sum() / 1024
)

memory_ports = (
    ports.memory_usage(deep=True).sum() / 1024
)

memory_after = (
    merged.memory_usage(deep=True).sum() / 1024
)


section("ZUZYCIE PAMIECI")

print(f"Titanic: {memory_before:.2f} KiB")
print(f"Ports: {memory_ports:.2f} KiB")
print(f"Po merge: {memory_after:.2f} KiB")

print(
    f"Wzrost: "
    f"{memory_after - memory_before:.2f} KiB"
)


# =========================================================
# 18. WNIOSKI
# =========================================================

section("WNIOSKI")

conclusions = [
    "Merge pozwala laczyc datasety wedlug wspolnego klucza.",
    "Left join zachowuje wszystkie rekordy lewej tabeli.",
    "Relacja many-to-one zapobiega powielaniu rekordow.",
    "Indicator pozwala sprawdzic dopasowanie rekordow.",
    "Dodano informacje o nazwie, kraju i rozmiarze portu.",
    "Brakujace porty pozostawiono jako NaN.",
    "GroupBy pozwala analizowac dane po polaczeniu tabel.",
    "Agg umozliwia obliczenie wielu statystyk jednoczesnie.",
    "Srednia Survived odpowiada wskaznikowi przezywalnosci.",
    "Najwyzsza przezywalnosc odnotowano w Cherbourg.",
    "Najwiecej pasazerow wsiadlo w Southampton.",
    "Struktura klas rozni sie pomiedzy portami.",
    "Rozmiar portu nie wykazuje monotonicznej zaleznosci.",
    "Kazdy rozmiar portu reprezentuje tylko jeden port.",
    "Country oznacza kraj portu, nie narodowosc.",
    "Zaleznosc statystyczna nie dowodzi przyczynowosci.",
    "Laczenie datasetow jest waznym elementem Data Science."
]

for number, conclusion in enumerate(
    conclusions,
    start=1
):
    print(f"{number}. {conclusion}")


# =========================================================
# 19. PODSUMOWANIE
# =========================================================

section("PODSUMOWANIE")

print(f"Liczba datasetow: 2")
print(f"Liczba pasazerow: {len(merged)}")
print(f"Liczba portow: {len(ports)}")
print(f"Liczba krajow: {ports['Country'].nunique()}")
print(f"Liczba rozmiarow: {ports['Port_Size'].nunique()}")
print(f"Dopasowane rekordy: {len(known_ports)}")
print(f"Niedopasowane rekordy: {len(unknown_ports)}")
print(f"Shape przed: {titanic.shape}")
print(f"Shape po: {merged.shape}")
print(f"Nowe kolumny: {len(new_columns)}")

print(
    f"Globalna przezywalnosc: "
    f"{global_survival:.2f}%"
)

print(
    f"Najlepszy port: "
    f"{best_port['Port_Name']} - "
    f"{best_port['Survival_Rate']:.2f}%"
)


# =========================================================
# 20. AUTOMATYCZNA WERYFIKACJA
# =========================================================

section("WERYFIKACJA")

expected_counts = {
    "Southampton": 644,
    "Cherbourg": 168,
    "Queenstown": 77
}

expected_survivors = {
    "Southampton": 217,
    "Cherbourg": 93,
    "Queenstown": 30
}

actual_counts = (
    port_stats.set_index("Port_Name")
    ["Liczba_pasazerow"].to_dict()
)

actual_survivors = (
    port_stats.set_index("Port_Name")
    ["Przezyli"].to_dict()
)

# Niezalezna weryfikacja srednich
means_correct = all(
    np.isclose(
        row["Sredni_wiek"],
        known_ports.loc[
            known_ports["Port_Name"] == row["Port_Name"],
            "Age"
        ].mean()
    )
    for _, row in port_stats.iterrows()
)

fares_correct = all(
    np.isclose(
        row["Srednia_oplata"],
        known_ports.loc[
            known_ports["Port_Name"] == row["Port_Name"],
            "Fare"
        ].mean()
    )
    for _, row in port_stats.iterrows()
)

rates_correct = all(
    np.isclose(
        row["Survival_Rate"],
        known_ports.loc[
            known_ports["Port_Name"] == row["Port_Name"],
            "Survived"
        ].mean() * 100
    )
    for _, row in port_stats.iterrows()
)

port_mapping = ports.set_index(
    "Embarked"
)["Port_Name"]

mapped_ports = merged["Embarked"].map(
    port_mapping
)

tests = {
    "Titanic ma 891 wierszy":
        len(titanic) == 891,

    "Titanic ma 12 kolumn":
        titanic.shape[1] == 12,

    "Ports ma shape (3, 4)":
        ports.shape == (3, 4),

    "Istnieja 3 porty":
        ports["Port_Name"].nunique() == 3,

    "Istnieja 3 kraje":
        ports["Country"].nunique() == 3,

    "Istnieja 3 rozmiary portow":
        ports["Port_Size"].nunique() == 3,

    "Klucz Embarked w Ports jest unikalny":
        ports["Embarked"].is_unique,

    "Merge zachowal 891 rekordow":
        len(merged) == 891,

    "Merge nie powielil pasazerow":
        merged["PassengerId"].is_unique,

    "Wynik ma shape (891, 15)":
        merged.shape == (891, 15),

    "Dodano 3 nowe kolumny":
        len(new_columns) == 3,

    "Dodano Port_Name":
        "Port_Name" in merged.columns,

    "Dodano Country":
        "Country" in merged.columns,

    "Dodano Port_Size":
        "Port_Size" in merged.columns,

    "Zachowano kolejnosc pasazerow":
        merged["PassengerId"].equals(
            titanic["PassengerId"]
        ),

    "Dopasowano 889 rekordow":
        len(known_ports) == 889,

    "Pozostaly 2 niedopasowane rekordy":
        len(unknown_ports) == 2,

    "Liczba brakujacych Port_Name wynosi 2":
        merged["Port_Name"].isna().sum() == 2,

    "Braki portow odpowiadaja brakom Embarked":
        merged["Port_Name"].isna().equals(
            merged["Embarked"].isna()
        ),

    "Mapowanie portow jest poprawne":
        mapped_ports.equals(
            merged["Port_Name"]
        ),

    "W znanych portach nie ma brakow Country":
        known_ports["Country"].notna().all(),

    "W znanych portach nie ma brakow Port_Size":
        known_ports["Port_Size"].notna().all(),

    "Utworzono 3 grupy portow":
        len(port_stats) == 3,

    "Utworzono 3 grupy rozmiarow":
        len(size_stats) == 3,

    "Utworzono 3 grupy krajow":
        len(country_stats) == 3,

    "Liczebnosci portow sa poprawne":
        actual_counts == expected_counts,

    "Liczby ocalalych sa poprawne":
        actual_survivors == expected_survivors,

    "Suma pasazerow w portach wynosi 889":
        port_stats["Liczba_pasazerow"].sum() == 889,

    "Suma ocalalych w portach wynosi 340":
        port_stats["Przezyli"].sum() == 340,

    "Globalna liczba ocalalych wynosi 342":
        merged["Survived"].sum() == 342,

    "Uwzgledniono wszystkich pasazerow":
        len(known_ports) + len(unknown_ports) == len(merged),

    "Przezyli i nie przezyli daja liczebnosc":
        (
            port_stats["Przezyli"]
            + port_stats["Nie_przezyli"]
            == port_stats["Liczba_pasazerow"]
        ).all(),

    "Przezywalnosc jest w zakresie 0-100":
        port_stats["Survival_Rate"].between(0, 100).all(),

    "Przezywalnosc i smiertelnosc daja 100":
        np.allclose(
            port_stats["Survival_Rate"]
            + port_stats["Mortality_Rate"],
            100
        ),

    "Udzialy portow sumuja sie do 100":
        np.isclose(
            port_stats["Udzial_pasazerow_%"].sum(),
            100
        ),

    "Srednie wieku obliczono poprawnie":
        means_correct,

    "Srednie oplaty obliczono poprawnie":
        fares_correct,

    "Przezywalnosc obliczono poprawnie":
        rates_correct,

    "Srednia wazona portow jest poprawna":
        np.isclose(
            weighted_survival,
            known_survival
        ),

    "Najwyzsza przezywalnosc ma Cherbourg":
        best_port["Port_Name"] == "Cherbourg",

    "Najnizsza przezywalnosc ma Southampton":
        worst_port["Port_Name"] == "Southampton",

    "Najwiecej pasazerow ma Southampton":
        largest_port["Port_Name"] == "Southampton",

    "Najwyzsza srednia oplata w Cherbourg":
        highest_fare["Port_Name"] == "Cherbourg",

    "Ranking jest poprawnie posortowany":
        ranking["Survival_Rate"].is_monotonic_decreasing,

    "Tabela klas uwzglednia 889 pasazerow":
        class_counts.to_numpy().sum() == 889,

    "Udzialy klas w portach daja 100":
        np.allclose(
            class_shares.sum(axis=1),
            100
        ),

    "Tabela plci uwzglednia 889 pasazerow":
        sex_counts.to_numpy().sum() == 889,

    "Agregacja wielopoziomowa zachowuje liczebnosc":
        multi_stats["Liczba_pasazerow"].sum() == 889,

    "Agregacja wielopoziomowa zachowuje ocalalych":
        multi_stats["Przezyli"].sum() == 340,

    "Tabela pivot zachowuje liczebnosc":
        survival_pivot["Razem"].sum() == 889,

    "Tabela pivot zachowuje ocalalych":
        survival_pivot["Przezyli"].sum() == 340,

    "Agregacja rozmiarow zachowuje liczebnosc":
        size_stats["Liczba_pasazerow"].sum() == 889,

    "Agregacja krajow zachowuje liczebnosc":
        country_stats["Liczba_pasazerow"].sum() == 889,

    "Istniejace kolumny pozostaly niezmienione":
        merged[titanic.columns].equals(titanic_original),

    "Oryginalny Titanic pozostal niezmieniony":
        titanic.equals(titanic_original),

    "Oryginalny Ports pozostal niezmieniony":
        ports.equals(ports_original)
}

passed = 0

for name, result in tests.items():
    result = bool(result)

    print(f"Czy {name}: {result}")

    if result:
        passed += 1

print(f"\nZaliczone testy: {passed}/{len(tests)}")

if passed == len(tests):
    print("Wszystkie testy zakonczone pomyslnie.")

else:
    raise AssertionError(
        "Nie wszystkie testy zostaly zaliczone."
    )
