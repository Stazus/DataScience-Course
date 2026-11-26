# Lekcja 13 - Zadanie 11: Zlozone filtrowanie

import sqlite3
import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# Pobranie datasetu Titanic
url = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

titanic = pd.read_csv(url)


# Utworzenie bazy danych SQLite w pamieci
conn = sqlite3.connect(":memory:")

# Zapis DataFrame do tabeli SQL
titanic.to_sql(
    "titanic",
    conn,
    index=False,
    if_exists="replace"
)


print("=" * 75)
print("ZLOZONE FILTROWANIE - ANALIZA PASAZEROW TITANICA")
print("=" * 75)


# 1. Dane wejsciowe
section("1. DANE WEJSCIOWE")

columns = [
    "PassengerId",
    "Pclass",
    "Sex",
    "Survived",
    "Age",
    "Fare"
]

print(titanic[columns].head(10).to_string(index=False))

print(f"\nLiczba pasazerow: {len(titanic)}")
print(f"Liczba kolumn: {len(titanic.columns)}")
print(f"Brakujace wartosci Age: {titanic['Age'].isna().sum()}")
print(f"Brakujace wartosci Fare: {titanic['Fare'].isna().sum()}")


# 2. Kobiety pierwszej klasy, ktore przezyly
section("2. KOBIETY Z 1 KLASY, KTORE PRZEZYLY")

query_women = """
SELECT
    PassengerId,
    Name,
    Pclass,
    Sex,
    Survived,
    Age,
    Fare
FROM titanic
WHERE Pclass = 1
    AND Sex = 'female'
    AND Survived = 1
ORDER BY Fare DESC, PassengerId ASC
"""

women = pd.read_sql_query(query_women, conn)

print(query_women)
print(women.head(10).to_string(index=False))

print(f"\nLiczba pasazerow: {len(women)}")
print(f"Sredni wiek: {women['Age'].mean():.2f}")
print(f"Srednia cena biletu: {women['Fare'].mean():.2f}")


# 3. Mezczyzni trzeciej klasy, ktorzy nie przezyli
section("3. MEZCZYZNI Z 3 KLASY, KTORZY NIE PRZEZYLI")

query_men = """
SELECT
    PassengerId,
    Name,
    Pclass,
    Sex,
    Survived,
    Age,
    Fare
FROM titanic
WHERE Pclass = 3
    AND Sex = 'male'
    AND Survived = 0
ORDER BY Fare DESC, PassengerId ASC
"""

men = pd.read_sql_query(query_men, conn)

print(query_men)
print(men.head(10).to_string(index=False))

print(f"\nLiczba pasazerow: {len(men)}")
print(f"Sredni wiek: {men['Age'].mean():.2f}")
print(f"Srednia cena biletu: {men['Fare'].mean():.2f}")


# 4. Agregacja SQL i UNION ALL
section("4. POROWNANIE GRUP - SQL UNION ALL")

query_comparison = """
SELECT
    'Kobiety 1 klasy - przezyly' AS grupa,
    COUNT(*) AS liczba,
    AVG(Age) AS avg_age,
    AVG(Fare) AS avg_fare
FROM titanic
WHERE Pclass = 1
    AND Sex = 'female'
    AND Survived = 1

UNION ALL

SELECT
    'Mezczyzni 3 klasy - nie przezyli' AS grupa,
    COUNT(*) AS liczba,
    AVG(Age) AS avg_age,
    AVG(Fare) AS avg_fare
FROM titanic
WHERE Pclass = 3
    AND Sex = 'male'
    AND Survived = 0
"""

comparison = pd.read_sql_query(
    query_comparison,
    conn
)

print(query_comparison)

print(
    comparison.round(2).to_string(index=False)
)


# 5. Tekstowy wykres cen biletow
section("5. TEKSTOWY WYKRES SREDNICH CEN BILETOW")

print("Legenda: jeden znak = 5 jednostek ceny Fare\n")

for row in comparison.itertuples(index=False):
    bar = "█" * round(row.avg_fare / 5)

    print(
        f"{row.grupa:35} | "
        f"{bar} {row.avg_fare:.2f}"
    )


# 6. Tekstowy wykres sredniego wieku
section("6. TEKSTOWY WYKRES SREDNIEGO WIEKU")

print("Legenda: jeden znak = okolo 1 rok\n")

for row in comparison.itertuples(index=False):
    bar = "█" * round(row.avg_age)

    print(
        f"{row.grupa:35} | "
        f"{bar} {row.avg_age:.2f} lat"
    )


# 7. Analiza roznic
section("7. ANALIZA ROZNIC MIEDZY GRUPAMI")

women_count = comparison.loc[0, "liczba"]
men_count = comparison.loc[1, "liczba"]

women_age = comparison.loc[0, "avg_age"]
men_age = comparison.loc[1, "avg_age"]

women_fare = comparison.loc[0, "avg_fare"]
men_fare = comparison.loc[1, "avg_fare"]

age_difference = women_age - men_age
fare_difference = women_fare - men_fare

fare_ratio = women_fare / men_fare

fare_difference_pct = (
    (women_fare - men_fare) / men_fare * 100
)

metrics = pd.DataFrame({
    "Metryka": [
        "Liczba kobiet",
        "Liczba mezczyzn",
        "Roznica sredniego wieku",
        "Roznica sredniej ceny biletu",
        "Stosunek srednich cen",
        "Roznica cen (%)"
    ],
    "Wartosc": [
        women_count,
        men_count,
        age_difference,
        fare_difference,
        fare_ratio,
        fare_difference_pct
    ]
})

print(metrics.round(2).to_string(index=False))

print(
    f"\nSrednia cena biletu kobiet z 1 klasy "
    f"byla {fare_ratio:.2f} razy wieksza "
    f"od sredniej ceny biletu mezczyzn z 3 klasy."
)


# 8. Analiza brakujacych wartosci
section("8. ANALIZA BRAKUJACYCH WARTOSCI")

missing = pd.DataFrame({
    "grupa": comparison["grupa"],
    "liczba_pasazerow": [
        len(women),
        len(men)
    ],
    "znany_wiek": [
        women["Age"].count(),
        men["Age"].count()
    ],
    "brakujacy_wiek": [
        women["Age"].isna().sum(),
        men["Age"].isna().sum()
    ],
    "brakujaca_cena": [
        women["Fare"].isna().sum(),
        men["Fare"].isna().sum()
    ]
})

print(missing.to_string(index=False))

print("\nCOUNT(*) uwzglednia wszystkie rekordy.")
print("AVG(Age) pomija wartosci NULL.")
print("Brakujacy wiek nie jest traktowany jako zero.")


# 9. Porownanie SQL z Pandas
section("9. WERYFIKACJA SQL ZA POMOCA PANDAS")

women_pd = titanic[
    (titanic["Pclass"] == 1)
    & (titanic["Sex"] == "female")
    & (titanic["Survived"] == 1)
]

men_pd = titanic[
    (titanic["Pclass"] == 3)
    & (titanic["Sex"] == "male")
    & (titanic["Survived"] == 0)
]

comparison_pd = pd.DataFrame({
    "grupa": [
        "Kobiety 1 klasy - przezyly",
        "Mezczyzni 3 klasy - nie przezyli"
    ],
    "liczba": [
        len(women_pd),
        len(men_pd)
    ],
    "avg_age": [
        women_pd["Age"].mean(),
        men_pd["Age"].mean()
    ],
    "avg_fare": [
        women_pd["Fare"].mean(),
        men_pd["Fare"].mean()
    ]
})

print(comparison_pd.round(2).to_string(index=False))

sql_pandas_equal = np.allclose(
    comparison[["liczba", "avg_age", "avg_fare"]],
    comparison_pd[["liczba", "avg_age", "avg_fare"]]
)

print(
    f"\nCzy SQL i Pandas zwracaja "
    f"identyczne wyniki: {sql_pandas_equal}"
)


# 10. Dodatkowa analiza przezywalnosci
section("10. PRZEZYWALNOSC WEDLUG KLASY I PLCI")

query_survival = """
SELECT
    Pclass,
    Sex,
    COUNT(*) AS passenger_count,
    SUM(Survived) AS survivors,
    AVG(Survived) * 100 AS survival_rate,
    AVG(Age) AS avg_age,
    AVG(Fare) AS avg_fare
FROM titanic
GROUP BY Pclass, Sex
ORDER BY Pclass, Sex
"""

survival = pd.read_sql_query(
    query_survival,
    conn
)

print(survival.round(2).to_string(index=False))


# 11. Plan wykonania zapytania
section("11. EXPLAIN QUERY PLAN")

plan = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_comparison,
    conn
)

print(plan.to_string(index=False))


# 12. Automatyczne testy
section("12. AUTOMATYCZNE TESTY")

original_count = pd.read_sql_query(
    "SELECT COUNT(*) AS liczba FROM titanic",
    conn
).loc[0, "liczba"]

tests = {
    "Dataset zawiera 891 pasazerow":
        len(titanic) == 891,

    "Identyfikatory pasazerow sa unikalne":
        titanic["PassengerId"].is_unique,

    "Pierwsza grupa nie jest pusta":
        len(women) > 0,

    "Druga grupa nie jest pusta":
        len(men) > 0,

    "Kobiety naleza do pierwszej klasy":
        women["Pclass"].eq(1).all(),

    "Pierwsza grupa zawiera tylko kobiety":
        women["Sex"].eq("female").all(),

    "Wszystkie kobiety z grupy przezyly":
        women["Survived"].eq(1).all(),

    "Mezczyzni naleza do trzeciej klasy":
        men["Pclass"].eq(3).all(),

    "Druga grupa zawiera tylko mezczyzn":
        men["Sex"].eq("male").all(),

    "Mezczyzni z grupy nie przezyli":
        men["Survived"].eq(0).all(),

    "Pierwsza grupa zawiera 91 pasazerow":
        len(women) == 91,

    "Druga grupa zawiera 300 pasazerow":
        len(men) == 300,

    "DataFrame porownawczy zawiera 2 wiersze":
        len(comparison) == 2,

    "DataFrame porownawczy zawiera 4 kolumny":
        comparison.shape[1] == 4,

    "Nazwy kolumn sa zgodne z wymaganiami":
        comparison.columns.tolist()
        == ["grupa", "liczba", "avg_age", "avg_fare"],

    "Liczba kobiet jest zgodna":
        women_count == len(women),

    "Liczba mezczyzn jest zgodna":
        men_count == len(men),

    "Sredni wiek kobiet jest poprawny":
        np.isclose(women_age, women["Age"].mean()),

    "Sredni wiek mezczyzn jest poprawny":
        np.isclose(men_age, men["Age"].mean()),

    "Srednia cena biletu kobiet jest poprawna":
        np.isclose(women_fare, women["Fare"].mean()),

    "Srednia cena biletu mezczyzn jest poprawna":
        np.isclose(men_fare, men["Fare"].mean()),

    "Brak NaN w tabeli porownawczej":
        not comparison.isna().any().any(),

    "Srednie ceny biletow sa dodatnie":
        comparison["avg_fare"].gt(0).all(),

    "Srednia cena biletu kobiet jest wyzsza":
        women_fare > men_fare,

    "Grupy nie zawieraja wspolnych pasazerow":
        set(women["PassengerId"]).isdisjoint(
            men["PassengerId"]
        ),

    "SQL i Pandas zwracaja zgodne wyniki":
        sql_pandas_equal,

    "Analiza przezywalnosci zawiera 6 grup":
        len(survival) == 6,

    "Przezywalnosc miesci sie w zakresie 0-100":
        survival["survival_rate"].between(0, 100).all(),

    "Oryginalna tabela pozostala niezmieniona":
        original_count == len(titanic)
}

for name, result in tests.items():
    print(f"Czy {name}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())
total = len(tests)

print(f"\nZaliczone testy: {passed}/{total}")


# 13. Wnioski
section("13. WNIOSKI")

conclusions = [
    "WHERE pozwala filtrowac dane wedlug wielu warunkow.",
    "AND wymaga jednoczesnego spelnienia wszystkich warunkow.",
    "COUNT(*) oblicza liczbe wszystkich pasazerow w grupie.",
    "AVG pomija brakujace wartosci NULL.",
    "UNION ALL laczy wyniki dwoch zapytan SELECT.",
    "Kobiety z pierwszej klasy placily srednio wiecej.",
    "Klasa pasazera jest zwiazana z cena biletu.",
    "Porownanie dwoch wybranych grup nie dowodzi przyczynowosci.",
    "Analiza przezywalnosci wymaga uwzglednienia wszystkich pasazerow.",
    "SQL i Pandas pozwalaja uzyskac zgodne wyniki.",
    "Filtrowanie SQL ogranicza liczbe pobieranych rekordow.",
    "EXPLAIN QUERY PLAN pokazuje sposob wykonania zapytania.",
    "Tekstowe slupki pozwalaja porownywac dane bez bibliotek graficznych."
]

for number, conclusion in enumerate(conclusions, 1):
    print(f"{number}. {conclusion}")


# 14. Podsumowanie
section("PODSUMOWANIE")

print(f"Liczba pasazerow: {len(titanic)}")
print(f"Kobiety z 1 klasy, ktore przezyly: {women_count}")
print(f"Mezczyzni z 3 klasy, ktorzy nie przezyli: {men_count}")
print(f"Sredni wiek kobiet: {women_age:.2f}")
print(f"Sredni wiek mezczyzn: {men_age:.2f}")
print(f"Srednia cena biletu kobiet: {women_fare:.2f}")
print(f"Srednia cena biletu mezczyzn: {men_fare:.2f}")
print(f"Stosunek srednich cen: {fare_ratio:.2f}x")
print(f"Zaliczone testy: {passed}/{total}")

conn.close()

assert passed == total, "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 11 wykonane poprawnie.")
