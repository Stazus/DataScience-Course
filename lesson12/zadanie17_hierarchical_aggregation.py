# Lekcja 12 - Zadanie 17: Hierarchical Aggregation

import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 100)


def text_bar(value, scale=2):
    """Tworzy tekstowy slupek procentowy."""
    return "█" * int(round(value / scale))


# ============================================================
# 1. KONFIGURACJA DATASETU
# ============================================================

np.random.seed(42)

records_per_city = 50

hierarchy = {
    "Europa": {
        "Polska": [
            "Warszawa", "Krakow", "Gdansk"
        ],
        "Niemcy": [
            "Berlin", "Hamburg", "Monachium"
        ],
        "Francja": [
            "Paryz", "Lyon", "Marsylia"
        ]
    },
    "Azja": {
        "Japonia": [
            "Tokio", "Osaka", "Kioto"
        ],
        "Chiny": [
            "Pekin", "Szanghaj", "Shenzhen"
        ],
        "Indie": [
            "Delhi", "Mumbai", "Bangalore"
        ]
    },
    "Ameryka Polnocna": {
        "USA": [
            "Nowy Jork", "Chicago", "Los Angeles"
        ],
        "Kanada": [
            "Toronto", "Vancouver", "Montreal"
        ],
        "Meksyk": [
            "Meksyk", "Guadalajara", "Monterrey"
        ]
    }
}


# ============================================================
# 2. GENEROWANIE DANYCH
# ============================================================

records = []

for continent, countries in hierarchy.items():

    for country, cities in countries.items():

        for city in cities:

            sales = np.random.randint(
                100, 10001, records_per_city
            )

            for value in sales:

                records.append({
                    "Kontynent": continent,
                    "Kraj": country,
                    "Miasto": city,
                    "Sprzedaż": int(value)
                })


df = pd.DataFrame(records)

df_original = df.copy(deep=True)

total_sales = df["Sprzedaż"].sum()

print("=" * 100)
print("HIERARCHICAL AGGREGATION - SPRZEDAZ MIEDZYNARODOWA")
print("=" * 100)


# ============================================================
# 3. DANE WEJSCIOWE
# ============================================================

section("DANE WEJSCIOWE")

print(f"Shape: {df.shape}")
print(f"Liczba rekordow: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print(f"Liczba kontynentow: {df['Kontynent'].nunique()}")
print(f"Liczba krajow: {df['Kraj'].nunique()}")
print(f"Liczba miast: {df['Miasto'].nunique()}")
print(f"Rekordy na miasto: {records_per_city}")
print(f"Liczba NaN: {df.isna().sum().sum()}")
print(f"Calkowita sprzedaz: {total_sales:,.2f}")
print("Seed: 42")
print("Dane syntetyczne: Tak")


section("PIERWSZE 10 REKORDOW")

print(df.head(10).to_string(index=False))


section("STATYSTYKI GLOBALNE SPRZEDAZY")

print(df["Sprzedaż"].describe().round(2))


section("LICZBA REKORDOW WEDLUG KONTYNENTU")

print(df.groupby("Kontynent").size())


section("LICZBA REKORDOW WEDLUG KRAJU")

print(df.groupby(["Kontynent", "Kraj"]).size())


# ============================================================
# 4. POZIOM 1 - KONTYNENT
# ============================================================

continents = (
    df.groupby("Kontynent")
    .agg(
        Liczba_rekordow=("Sprzedaż", "size"),
        Liczba_krajow=("Kraj", "nunique"),
        Liczba_miast=("Miasto", "nunique"),
        Suma_sprzedazy=("Sprzedaż", "sum"),
        Srednia_sprzedaz=("Sprzedaż", "mean"),
        Mediana_sprzedazy=("Sprzedaż", "median"),
        Minimum=("Sprzedaż", "min"),
        Maksimum=("Sprzedaż", "max"),
        Odchylenie_std=("Sprzedaż", "std")
    )
    .reset_index()
)

continents["Udzial_globalny_%"] = (
    continents["Suma_sprzedazy"] / total_sales * 100
)

continents = continents.sort_values(
    "Suma_sprzedazy", ascending=False
).reset_index(drop=True)


section("POZIOM 1 - AGREGACJA WEDLUG KONTYNENTU")

print(continents.round(2).to_string(index=False))


# ============================================================
# 5. POZIOM 2 - KRAJ
# ============================================================

countries = (
    df.groupby(["Kontynent", "Kraj"])
    .agg(
        Liczba_rekordow=("Sprzedaż", "size"),
        Liczba_miast=("Miasto", "nunique"),
        Suma_sprzedazy=("Sprzedaż", "sum"),
        Srednia_sprzedaz=("Sprzedaż", "mean"),
        Mediana_sprzedazy=("Sprzedaż", "median"),
        Minimum=("Sprzedaż", "min"),
        Maksimum=("Sprzedaż", "max"),
        Odchylenie_std=("Sprzedaż", "std")
    )
    .reset_index()
)

countries["Sprzedaz_kontynentu"] = (
    countries.groupby("Kontynent")["Suma_sprzedazy"]
    .transform("sum")
)

countries["Udzial_w_kontynencie_%"] = (
    countries["Suma_sprzedazy"]
    / countries["Sprzedaz_kontynentu"]
    * 100
)

countries["Udzial_globalny_%"] = (
    countries["Suma_sprzedazy"] / total_sales * 100
)

countries = countries.sort_values(
    ["Kontynent", "Suma_sprzedazy"],
    ascending=[True, False]
).reset_index(drop=True)


section("POZIOM 2 - AGREGACJA WEDLUG KRAJU")

print(countries.round(2).to_string(index=False))


# ============================================================
# 6. POZIOM 3 - MIASTO
# ============================================================

cities = (
    df.groupby(["Kontynent", "Kraj", "Miasto"])
    .agg(
        Liczba_rekordow=("Sprzedaż", "size"),
        Suma_sprzedazy=("Sprzedaż", "sum"),
        Srednia_sprzedaz=("Sprzedaż", "mean"),
        Mediana_sprzedazy=("Sprzedaż", "median"),
        Minimum=("Sprzedaż", "min"),
        Maksimum=("Sprzedaż", "max"),
        Odchylenie_std=("Sprzedaż", "std")
    )
    .reset_index()
)

cities["Sprzedaz_kraju"] = (
    cities.groupby(
        ["Kontynent", "Kraj"]
    )["Suma_sprzedazy"]
    .transform("sum")
)

cities["Sprzedaz_kontynentu"] = (
    cities.groupby("Kontynent")["Suma_sprzedazy"]
    .transform("sum")
)

cities["Udzial_w_kraju_%"] = (
    cities["Suma_sprzedazy"]
    / cities["Sprzedaz_kraju"]
    * 100
)

cities["Udzial_w_kontynencie_%"] = (
    cities["Suma_sprzedazy"]
    / cities["Sprzedaz_kontynentu"]
    * 100
)

cities["Udzial_globalny_%"] = (
    cities["Suma_sprzedazy"] / total_sales * 100
)

cities = cities.sort_values(
    ["Kontynent", "Kraj", "Suma_sprzedazy"],
    ascending=[True, True, False]
).reset_index(drop=True)


section("POZIOM 3 - AGREGACJA WEDLUG MIASTA")

print(cities.round(2).to_string(index=False))


# ============================================================
# 7. STRUKTURA HIERARCHII
# ============================================================

section("STRUKTURA HIERARCHII")

print(f"Poziom 1 - kontynenty: {len(continents)}")
print(f"Poziom 2 - kraje: {len(countries)}")
print(f"Poziom 3 - miasta: {len(cities)}")

print(
    f"Laczna liczba wezlow: "
    f"{len(continents) + len(countries) + len(cities)}"
)

print(f"Shape continents: {continents.shape}")
print(f"Shape countries: {countries.shape}")
print(f"Shape cities: {cities.shape}")


# ============================================================
# 8. TEKSTOWE DRZEWO HIERARCHICZNE
# ============================================================

section("TEKSTOWE DRZEWO SPRZEDAZY")

print(f"SWIAT | {total_sales:,.2f} | 100.00%")

for continent_index, continent in continents.iterrows():

    continent_name = continent["Kontynent"]

    continent_last = (
        continent_index == len(continents) - 1
    )

    continent_branch = "└── " if continent_last else "├── "
    continent_prefix = "    " if continent_last else "│   "

    print(
        f"{continent_branch}{continent_name} | "
        f"{continent['Suma_sprzedazy']:,.2f} | "
        f"{continent['Udzial_globalny_%']:.2f}% swiata"
    )

    continent_countries = (
        countries[
            countries["Kontynent"] == continent_name
        ]
        .sort_values("Suma_sprzedazy", ascending=False)
        .reset_index(drop=True)
    )

    for country_index, country in continent_countries.iterrows():

        country_name = country["Kraj"]

        country_last = (
            country_index == len(continent_countries) - 1
        )

        country_branch = "└── " if country_last else "├── "
        country_prefix = "    " if country_last else "│   "

        print(
            f"{continent_prefix}{country_branch}"
            f"{country_name} | "
            f"{country['Suma_sprzedazy']:,.2f} | "
            f"{country['Udzial_w_kontynencie_%']:.2f}% kontynentu | "
            f"{country['Udzial_globalny_%']:.2f}% swiata"
        )

        country_cities = (
            cities[
                (cities["Kontynent"] == continent_name)
                & (cities["Kraj"] == country_name)
            ]
            .sort_values("Suma_sprzedazy", ascending=False)
            .reset_index(drop=True)
        )

        for city_index, city in country_cities.iterrows():

            city_last = (
                city_index == len(country_cities) - 1
            )

            city_branch = "└── " if city_last else "├── "

            print(
                f"{continent_prefix}{country_prefix}"
                f"{city_branch}{city['Miasto']} | "
                f"{city['Suma_sprzedazy']:,.2f} | "
                f"{city['Udzial_w_kraju_%']:.2f}% kraju | "
                f"{city['Udzial_globalny_%']:.2f}% swiata"
            )


# ============================================================
# 9. RANKING KONTYNENTOW
# ============================================================

section("RANKING KONTYNENTOW")

continent_ranking = continents[
    [
        "Kontynent",
        "Suma_sprzedazy",
        "Srednia_sprzedaz",
        "Udzial_globalny_%"
    ]
].sort_values("Suma_sprzedazy", ascending=False)

print(continent_ranking.round(2).to_string(index=False))


# ============================================================
# 10. RANKING KRAJOW
# ============================================================

section("RANKING KRAJOW")

country_ranking = countries[
    [
        "Kontynent",
        "Kraj",
        "Suma_sprzedazy",
        "Udzial_w_kontynencie_%",
        "Udzial_globalny_%"
    ]
].sort_values("Suma_sprzedazy", ascending=False)

print(country_ranking.round(2).to_string(index=False))


# ============================================================
# 11. TOP 10 MIAST
# ============================================================

section("TOP 10 MIAST WEDLUG SPRZEDAZY")

city_ranking = cities[
    [
        "Kontynent",
        "Kraj",
        "Miasto",
        "Suma_sprzedazy",
        "Udzial_w_kraju_%",
        "Udzial_globalny_%"
    ]
].sort_values("Suma_sprzedazy", ascending=False)

print(city_ranking.head(10).round(2).to_string(index=False))


section("BOTTOM 10 MIAST WEDLUG SPRZEDAZY")

print(
    city_ranking.sort_values("Suma_sprzedazy")
    .head(10)
    .round(2)
    .to_string(index=False)
)


# ============================================================
# 12. TEKSTOWE WYKRESY
# ============================================================

section("TEKSTOWY WYKRES UDZIALU KONTYNENTOW")

print("Legenda: jeden znak = okolo 2% sprzedazy globalnej")

for _, row in continent_ranking.iterrows():

    value = row["Udzial_globalny_%"]

    print(
        f"{row['Kontynent']:<20} | "
        f"{text_bar(value):<50} {value:6.2f}%"
    )


section("TEKSTOWY WYKRES UDZIALU KRAJOW")

print("Legenda: jeden znak = okolo 1% sprzedazy globalnej")

for _, row in country_ranking.iterrows():

    value = row["Udzial_globalny_%"]

    print(
        f"{row['Kraj']:<15} | "
        f"{text_bar(value, scale=1):<25} {value:6.2f}%"
    )


section("TEKSTOWY WYKRES TOP 10 MIAST")

print("Legenda: jeden znak = okolo 0.2% sprzedazy globalnej")

for _, row in city_ranking.head(10).iterrows():

    value = row["Udzial_globalny_%"]

    print(
        f"{row['Miasto']:<15} | "
        f"{text_bar(value, scale=0.2):<30} {value:6.2f}%"
    )


# ============================================================
# 13. WERYFIKACJA UDZIALOW PROCENTOWYCH
# ============================================================

section("SUMA UDZIALOW KONTYNENTOW")

print(
    f"{continents['Udzial_globalny_%'].sum():.4f}%"
)


section("SUMA UDZIALOW KRAJOW W KONTYNENTACH")

country_shares = (
    countries.groupby("Kontynent")["Udzial_w_kontynencie_%"]
    .sum()
)

print(country_shares.round(4))


section("SUMA UDZIALOW MIAST W KRAJACH")

city_shares = (
    cities.groupby(
        ["Kontynent", "Kraj"]
    )["Udzial_w_kraju_%"]
    .sum()
)

print(city_shares.round(4))


section("SUMA UDZIALOW MIAST W KONTYNENTACH")

city_continent_shares = (
    cities.groupby(
        "Kontynent"
    )["Udzial_w_kontynencie_%"]
    .sum()
)

print(city_continent_shares.round(4))


section("GLOBALNE UDZIALY NA KAZDYM POZIOMIE")

print(
    f"Kontynenty: "
    f"{continents['Udzial_globalny_%'].sum():.4f}%"
)

print(
    f"Kraje: "
    f"{countries['Udzial_globalny_%'].sum():.4f}%"
)

print(
    f"Miasta: "
    f"{cities['Udzial_globalny_%'].sum():.4f}%"
)


# ============================================================
# 14. KONTROLA SPOJNOSCI HIERARCHII
# ============================================================

section("KONTROLA SPOJNOSCI HIERARCHII")

print(f"Dataset:    {total_sales:,.2f}")

print(
    f"Kontynenty: "
    f"{continents['Suma_sprzedazy'].sum():,.2f}"
)

print(
    f"Kraje:      "
    f"{countries['Suma_sprzedazy'].sum():,.2f}"
)

print(
    f"Miasta:     "
    f"{cities['Suma_sprzedazy'].sum():,.2f}"
)


country_to_continent = (
    countries.groupby("Kontynent")["Suma_sprzedazy"]
    .sum()
    .sort_index()
)

continent_direct = (
    continents.set_index("Kontynent")["Suma_sprzedazy"]
    .sort_index()
)

city_to_country = (
    cities.groupby(["Kontynent", "Kraj"])["Suma_sprzedazy"]
    .sum()
    .sort_index()
)

country_direct = (
    countries.set_index(
        ["Kontynent", "Kraj"]
    )["Suma_sprzedazy"]
    .sort_index()
)

city_to_continent = (
    cities.groupby("Kontynent")["Suma_sprzedazy"]
    .sum()
    .sort_index()
)


section("POROWNANIE SUM KRAJOW Z KONTYNENTAMI")

comparison_continents = pd.DataFrame({
    "Suma_krajow": country_to_continent,
    "Suma_kontynentu": continent_direct
})

comparison_continents["Roznica"] = (
    comparison_continents["Suma_krajow"]
    - comparison_continents["Suma_kontynentu"]
)

print(comparison_continents.to_string())


section("POROWNANIE SUM MIAST Z KRAJAMI")

comparison_countries = pd.DataFrame({
    "Suma_miast": city_to_country,
    "Suma_kraju": country_direct
})

comparison_countries["Roznica"] = (
    comparison_countries["Suma_miast"]
    - comparison_countries["Suma_kraju"]
)

print(comparison_countries.to_string())


# ============================================================
# 15. WAZONE SREDNIE
# ============================================================

section("WERYFIKACJA SREDNICH WAZONYCH")

global_mean = df["Sprzedaż"].mean()

weighted_continents = np.average(
    continents["Srednia_sprzedaz"],
    weights=continents["Liczba_rekordow"]
)

weighted_countries = np.average(
    countries["Srednia_sprzedaz"],
    weights=countries["Liczba_rekordow"]
)

weighted_cities = np.average(
    cities["Srednia_sprzedaz"],
    weights=cities["Liczba_rekordow"]
)

print(f"Srednia globalna: {global_mean:.6f}")
print(f"Srednia wazona kontynentow: {weighted_continents:.6f}")
print(f"Srednia wazona krajow: {weighted_countries:.6f}")
print(f"Srednia wazona miast: {weighted_cities:.6f}")


# ============================================================
# 16. ANALIZA NAJLEPSZYCH GRUP
# ============================================================

section("NAJLEPSZE GRUPY SPRZEDAZOWE")

best_continent = continents.loc[
    continents["Suma_sprzedazy"].idxmax()
]

best_country = countries.loc[
    countries["Suma_sprzedazy"].idxmax()
]

best_city = cities.loc[
    cities["Suma_sprzedazy"].idxmax()
]

worst_city = cities.loc[
    cities["Suma_sprzedazy"].idxmin()
]

print(
    f"Najlepszy kontynent: "
    f"{best_continent['Kontynent']} - "
    f"{best_continent['Suma_sprzedazy']:,.2f}"
)

print(
    f"Najlepszy kraj: "
    f"{best_country['Kraj']} - "
    f"{best_country['Suma_sprzedazy']:,.2f}"
)

print(
    f"Najlepsze miasto: "
    f"{best_city['Miasto']} - "
    f"{best_city['Suma_sprzedazy']:,.2f}"
)

print(
    f"Najnizsza sprzedaz miasta: "
    f"{worst_city['Miasto']} - "
    f"{worst_city['Suma_sprzedazy']:,.2f}"
)

print(
    f"Roznica pomiedzy najlepszym i najgorszym miastem: "
    f"{best_city['Suma_sprzedazy'] - worst_city['Suma_sprzedazy']:,.2f}"
)


# ============================================================
# 17. KONCENTRACJA SPRZEDAZY
# ============================================================

section("KONCENTRACJA SPRZEDAZY")

for top_n in [1, 3, 5, 10]:

    top_share = (
        city_ranking.head(top_n)["Suma_sprzedazy"].sum()
        / total_sales
        * 100
    )

    print(
        f"Top {top_n:2d} miast: "
        f"{top_share:.2f}% sprzedazy globalnej"
    )


# ============================================================
# 18. ZUZYCIE PAMIECI
# ============================================================

section("ZUZYCIE PAMIECI")

original_memory = df.memory_usage(deep=True).sum()

continents_memory = (
    continents.memory_usage(deep=True).sum()
)

countries_memory = (
    countries.memory_usage(deep=True).sum()
)

cities_memory = (
    cities.memory_usage(deep=True).sum()
)

aggregated_memory = (
    continents_memory
    + countries_memory
    + cities_memory
)

print(f"Dataset: {original_memory / 1024:.2f} KiB")
print(f"Kontynenty: {continents_memory / 1024:.2f} KiB")
print(f"Kraje: {countries_memory / 1024:.2f} KiB")
print(f"Miasta: {cities_memory / 1024:.2f} KiB")

print(
    f"Wszystkie agregacje: "
    f"{aggregated_memory / 1024:.2f} KiB"
)

print(
    f"Rozmiar agregacji wzgledem datasetu: "
    f"{aggregated_memory / original_memory * 100:.2f}%"
)


# ============================================================
# 19. WNIOSKI
# ============================================================

section("WNIOSKI")

conclusions = [
    "Hierarchical Aggregation agreguje dane na wielu poziomach.",
    "Utworzono hierarchie kontynent -> kraj -> miasto.",
    "GroupBy pozwala grupowac wedlug wielu kolumn.",
    "Agg pozwala obliczac wiele statystyk jednoczesnie.",
    "Transform pozwala przypisac sumy grup nadrzednych.",
    "Contribution okresla procentowy wklad grupy.",
    "Udzialy grup podrzednych sumuja sie do 100%.",
    "Udzial globalny pozwala porownywac rozne poziomy.",
    "Reset_index splaszcza strukture MultiIndex.",
    "Tekstowe drzewo przedstawia hierarchie bez bibliotek graficznych.",
    "Sumy sprzedazy musza byc zgodne na kazdym poziomie.",
    "Srednie grupowe mozna laczyc przez srednia wazona.",
    "Agregacja redukuje liczbe rekordow.",
    "Hierarchiczne raporty sa przydatne w Business Intelligence.",
    "Dane sa syntetyczne i nie opisuja rzeczywistej sprzedazy."
]

for number, conclusion in enumerate(conclusions, start=1):

    print(f"{number}. {conclusion}")


# ============================================================
# 20. PODSUMOWANIE
# ============================================================

section("PODSUMOWANIE")

print(f"Liczba rekordow: {len(df)}")
print(f"Liczba kontynentow: {len(continents)}")
print(f"Liczba krajow: {len(countries)}")
print(f"Liczba miast: {len(cities)}")
print(f"Rekordy na miasto: {records_per_city}")
print("Liczba poziomow agregacji: 3")
print(f"Calkowita sprzedaz: {total_sales:,.2f}")
print(f"Srednia sprzedaz: {global_mean:,.2f}")
print(f"Najlepszy kontynent: {best_continent['Kontynent']}")
print(f"Najlepszy kraj: {best_country['Kraj']}")
print(f"Najlepsze miasto: {best_city['Miasto']}")


# ============================================================
# 21. TESTY POPRAWNOSCI
# ============================================================

section("WERYFIKACJA")

expected_columns = [
    "Kontynent", "Kraj", "Miasto", "Sprzedaż"
]

tests = {
    "Dataset ma 1350 rekordow":
        len(df) == 1350,

    "Dataset ma 4 kolumny":
        df.shape[1] == 4,

    "Nazwy kolumn sa poprawne":
        df.columns.tolist() == expected_columns,

    "Dataset nie zawiera NaN":
        not df.isna().any().any(),

    "Sprzedaz ma typ numeryczny":
        pd.api.types.is_numeric_dtype(df["Sprzedaż"]),

    "Sprzedaz jest dodatnia":
        (df["Sprzedaż"] > 0).all(),

    "Sprzedaz miesci sie w zakresie 100-10000":
        df["Sprzedaż"].between(100, 10000).all(),

    "Istnieja 3 kontynenty":
        df["Kontynent"].nunique() == 3,

    "Istnieje 9 krajow":
        df["Kraj"].nunique() == 9,

    "Istnieje 27 miast":
        df["Miasto"].nunique() == 27,

    "Kazdy kontynent ma 3 kraje":
        df.groupby("Kontynent")["Kraj"].nunique().eq(3).all(),

    "Kazdy kraj ma 3 miasta":
        df.groupby(
            ["Kontynent", "Kraj"]
        )["Miasto"].nunique().eq(3).all(),

    "Kazde miasto ma 50 rekordow":
        df.groupby(
            ["Kontynent", "Kraj", "Miasto"]
        ).size().eq(50).all(),

    "Kazdy kraj ma 150 rekordow":
        df.groupby(
            ["Kontynent", "Kraj"]
        ).size().eq(150).all(),

    "Kazdy kontynent ma 450 rekordow":
        df.groupby("Kontynent").size().eq(450).all(),

    "Agregacja kontynentow ma 3 wiersze":
        len(continents) == 3,

    "Agregacja krajow ma 9 wierszy":
        len(countries) == 9,

    "Agregacja miast ma 27 wierszy":
        len(cities) == 27,

    "Agregacje sa DataFrame":
        all(
            isinstance(table, pd.DataFrame)
            for table in [continents, countries, cities]
        ),

    "Indeks kontynentow zostal splaszczony":
        not isinstance(continents.index, pd.MultiIndex),

    "Indeks krajow zostal splaszczony":
        not isinstance(countries.index, pd.MultiIndex),

    "Indeks miast zostal splaszczony":
        not isinstance(cities.index, pd.MultiIndex),

    "Kontynenty nie zawieraja NaN":
        not continents.isna().any().any(),

    "Kraje nie zawieraja NaN":
        not countries.isna().any().any(),

    "Miasta nie zawieraja NaN":
        not cities.isna().any().any(),

    "Suma sprzedazy kontynentow jest poprawna":
        continents["Suma_sprzedazy"].sum() == total_sales,

    "Suma sprzedazy krajow jest poprawna":
        countries["Suma_sprzedazy"].sum() == total_sales,

    "Suma sprzedazy miast jest poprawna":
        cities["Suma_sprzedazy"].sum() == total_sales,

    "Kontynenty uwzgledniaja wszystkie rekordy":
        continents["Liczba_rekordow"].sum() == len(df),

    "Kraje uwzgledniaja wszystkie rekordy":
        countries["Liczba_rekordow"].sum() == len(df),

    "Miasta uwzgledniaja wszystkie rekordy":
        cities["Liczba_rekordow"].sum() == len(df),

    "Globalne udzialy kontynentow daja 100%":
        np.isclose(
            continents["Udzial_globalny_%"].sum(), 100
        ),

    "Globalne udzialy krajow daja 100%":
        np.isclose(
            countries["Udzial_globalny_%"].sum(), 100
        ),

    "Globalne udzialy miast daja 100%":
        np.isclose(
            cities["Udzial_globalny_%"].sum(), 100
        ),

    "Udzialy krajow w kontynentach daja 100%":
        np.allclose(country_shares, 100),

    "Udzialy miast w krajach daja 100%":
        np.allclose(city_shares, 100),

    "Udzialy miast w kontynentach daja 100%":
        np.allclose(city_continent_shares, 100),

    "Udzialy kontynentow sa w zakresie 0-100":
        continents["Udzial_globalny_%"].between(0, 100).all(),

    "Udzialy krajow sa w zakresie 0-100":
        countries["Udzial_w_kontynencie_%"].between(0, 100).all(),

    "Udzialy miast sa w zakresie 0-100":
        cities["Udzial_w_kraju_%"].between(0, 100).all(),

    "Sumy krajow odpowiadaja sumom kontynentow":
        country_to_continent.equals(continent_direct),

    "Sumy miast odpowiadaja sumom krajow":
        city_to_country.equals(country_direct),

    "Sumy miast odpowiadaja sumom kontynentow":
        city_to_continent.equals(continent_direct),

    "Roznice sum kontynentow wynosza zero":
        comparison_continents["Roznica"].eq(0).all(),

    "Roznice sum krajow wynosza zero":
        comparison_countries["Roznica"].eq(0).all(),

    "Srednia wazona kontynentow jest poprawna":
        np.isclose(weighted_continents, global_mean),

    "Srednia wazona krajow jest poprawna":
        np.isclose(weighted_countries, global_mean),

    "Srednia wazona miast jest poprawna":
        np.isclose(weighted_cities, global_mean),

    "Ranking kontynentow jest poprawny":
        continent_ranking["Suma_sprzedazy"].is_monotonic_decreasing,

    "Ranking krajow jest poprawny":
        country_ranking["Suma_sprzedazy"].is_monotonic_decreasing,

    "Ranking miast jest poprawny":
        city_ranking["Suma_sprzedazy"].is_monotonic_decreasing,

    "Top 10 zawiera 10 miast":
        len(city_ranking.head(10)) == 10,

    "Najlepsze miasto ma maksymalna sprzedaz":
        best_city["Suma_sprzedazy"] == cities["Suma_sprzedazy"].max(),

    "Najgorsze miasto ma minimalna sprzedaz":
        worst_city["Suma_sprzedazy"] == cities["Suma_sprzedazy"].min(),

    "Agregacje maja mniej wierszy niz dataset":
        all(
            len(table) < len(df)
            for table in [continents, countries, cities]
        ),

    "Oryginalne dane pozostaly niezmienione":
        df.equals(df_original)
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

    print("Nie wszystkie testy zostaly zaliczone.")

assert passed == len(tests), "Weryfikacja nie powiodla sie."

