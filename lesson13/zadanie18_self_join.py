# Lekcja 13 - Zadanie 18: Self-JOIN

import sqlite3
import pandas as pd
import numpy as np


def section(title):
    """Wyswietla naglowek sekcji."""
    print(f"\n{title}")
    print("=" * 90)


def show_table(df):
    """Wyswietla DataFrame bez indeksu."""
    print(df.to_string(index=False))


# Utworzenie bazy danych SQLite w pamieci
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")


# Utworzenie tabeli employees
cursor.execute("""
    CREATE TABLE employees (
        employee_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        manager_id INTEGER,
        FOREIGN KEY (manager_id)
            REFERENCES employees(employee_id),
        CHECK (manager_id <> employee_id)
    )
""")


# Przygotowanie hierarchii organizacyjnej
employees = [
    (1, "Anna", None),
    (2, "Piotr", 1),
    (3, "Maria", 1),
    (4, "Jan", 1),
    (5, "Katarzyna", 1),
    (6, "Adam", 2),
    (7, "Ewa", 2),
    (8, "Kamil", 2),
    (9, "Ola", 3),
    (10, "Tomasz", 3),
    (11, "Karol", 4),
    (12, "Marta", 4),
    (13, "Pawel", 4),
    (14, "Julia", 5),
    (15, "Robert", 5)
]


cursor.executemany("""
    INSERT INTO employees (
        employee_id,
        name,
        manager_id
    )
    VALUES (?, ?, ?)
""", employees)

conn.commit()


print("=" * 90)
print("SELF-JOIN - HIERARCHIA ORGANIZACYJNA")
print("=" * 90)


# 1. Dane wejsciowe
section("1. TABELA EMPLOYEES")

employees_df = pd.read_sql_query("""
    SELECT *
    FROM employees
    ORDER BY employee_id
""", conn)

show_table(employees_df)

print(f"\nLiczba pracownikow: {len(employees_df)}")


# 2. SELF JOIN
section("2. PRACOWNICY I ICH MANAGEROWIE")

query_self_join = """
SELECT
    e1.employee_id,
    e1.name AS employee,
    e2.name AS manager
FROM employees AS e1
LEFT JOIN employees AS e2
    ON e1.manager_id = e2.employee_id
ORDER BY e1.employee_id
"""

print(query_self_join)

self_join_df = pd.read_sql_query(
    query_self_join,
    conn
)

show_table(self_join_df)

print(f"\nLiczba wynikow: {len(self_join_df)}")


# 3. SELF JOIN z COALESCE
section("3. SELF JOIN Z COALESCE")

query_coalesce = """
SELECT
    e1.employee_id,
    e1.name AS employee,
    COALESCE(
        e2.name,
        'TOP Management'
    ) AS manager
FROM employees AS e1
LEFT JOIN employees AS e2
    ON e1.manager_id = e2.employee_id
ORDER BY e1.employee_id
"""

print(query_coalesce)

coalesce_df = pd.read_sql_query(
    query_coalesce,
    conn
)

show_table(coalesce_df)


# 4. TOP management
section("4. PRACOWNICY BEZ MANAGERA")

query_top = """
SELECT
    employee_id,
    name,
    manager_id
FROM employees
WHERE manager_id IS NULL
ORDER BY employee_id
"""

print(query_top)

top_df = pd.read_sql_query(
    query_top,
    conn
)

show_table(top_df)

print(
    f"\nLiczba osob w TOP management: "
    f"{len(top_df)}"
)


# 5. Liczba bezposrednich podwladnych
section("5. LICZBA PODWLADNYCH KAZDEGO MANAGERA")

query_managers = """
SELECT
    m.employee_id AS manager_id,
    m.name AS manager,
    COUNT(e.employee_id) AS subordinates
FROM employees AS m
INNER JOIN employees AS e
    ON m.employee_id = e.manager_id
GROUP BY
    m.employee_id,
    m.name
ORDER BY
    subordinates DESC,
    m.employee_id ASC
"""

print(query_managers)

managers_df = pd.read_sql_query(
    query_managers,
    conn
)

show_table(managers_df)

print(f"\nLiczba managerow: {len(managers_df)}")

print(
    "Laczna liczba bezposrednich podwladnych: "
    f"{managers_df['subordinates'].sum()}"
)


# 6. Wszyscy pracownicy i liczba podwladnych
section("6. WSZYSCY PRACOWNICY I LICZBA PODWLADNYCH")

query_all = """
SELECT
    m.employee_id,
    m.name,
    COUNT(e.employee_id) AS subordinates
FROM employees AS m
LEFT JOIN employees AS e
    ON m.employee_id = e.manager_id
GROUP BY
    m.employee_id,
    m.name
ORDER BY
    subordinates DESC,
    m.employee_id ASC
"""

print(query_all)

all_df = pd.read_sql_query(
    query_all,
    conn
)

show_table(all_df)


# 7. Pracownicy bez podwladnych
section("7. PRACOWNICY BEZ PODWLADNYCH")

query_no_subordinates = """
SELECT
    m.employee_id,
    m.name
FROM employees AS m
LEFT JOIN employees AS e
    ON m.employee_id = e.manager_id
WHERE e.employee_id IS NULL
ORDER BY m.employee_id
"""

no_subordinates_df = pd.read_sql_query(
    query_no_subordinates,
    conn
)

show_table(no_subordinates_df)

print(
    "\nLiczba pracownikow bez podwladnych: "
    f"{len(no_subordinates_df)}"
)


# 8. Klasyfikacja pracownikow
section("8. KLASYFIKACJA PRACOWNIKOW")

query_classification = """
SELECT
    m.employee_id,
    m.name,
    COUNT(e.employee_id) AS subordinates,

    CASE
        WHEN m.manager_id IS NULL
            THEN 'TOP Management'

        WHEN COUNT(e.employee_id) > 0
            THEN 'Manager'

        ELSE 'Employee'
    END AS role

FROM employees AS m
LEFT JOIN employees AS e
    ON m.employee_id = e.manager_id

GROUP BY
    m.employee_id,
    m.name,
    m.manager_id

ORDER BY m.employee_id
"""

classification_df = pd.read_sql_query(
    query_classification,
    conn
)

show_table(classification_df)


# 9. Podsumowanie stanowisk
section("9. PODSUMOWANIE STRUKTURY ORGANIZACYJNEJ")

roles_df = (
    classification_df
    .groupby("role")
    .size()
    .reset_index(name="employees_count")
)

roles_df["percentage"] = (
    roles_df["employees_count"]
    / len(employees_df)
    * 100
)

show_table(roles_df.round(2))


# 10. Tekstowy wykres liczby podwladnych
section("10. TEKSTOWY WYKRES LICZBY PODWLADNYCH")

print("Legenda: jeden znak = jeden podwladny\n")

for row in managers_df.itertuples(index=False):
    bar = "█" * int(row.subordinates)

    print(
        f"{row.manager:<15} | "
        f"{bar:<10} "
        f"{row.subordinates}"
    )


# 11. Porownanie INNER JOIN i LEFT JOIN
section("11. POROWNANIE INNER JOIN I LEFT JOIN")

query_inner = """
SELECT
    e1.employee_id,
    e1.name AS employee,
    e2.name AS manager
FROM employees AS e1
INNER JOIN employees AS e2
    ON e1.manager_id = e2.employee_id
ORDER BY e1.employee_id
"""

inner_df = pd.read_sql_query(
    query_inner,
    conn
)

comparison_df = pd.DataFrame({
    "join_type": [
        "INNER JOIN",
        "LEFT JOIN"
    ],
    "rows": [
        len(inner_df),
        len(self_join_df)
    ],
    "missing_managers": [
        inner_df["manager"].isna().sum(),
        self_join_df["manager"].isna().sum()
    ]
})

show_table(comparison_df)


# 12. Hierarchia wielopoziomowa - recursive CTE
section("12. PELNA HIERARCHIA ORGANIZACYJNA")

query_hierarchy = """
WITH RECURSIVE hierarchy AS (

    SELECT
        employee_id,
        name,
        manager_id,
        0 AS level,
        name AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT
        e.employee_id,
        e.name,
        e.manager_id,
        h.level + 1,
        h.path || ' > ' || e.name
    FROM employees AS e
    INNER JOIN hierarchy AS h
        ON e.manager_id = h.employee_id

)
SELECT *
FROM hierarchy
ORDER BY path
"""

print(query_hierarchy)

hierarchy_df = pd.read_sql_query(
    query_hierarchy,
    conn
)

show_table(hierarchy_df)

print("\nDrzewo organizacyjne:\n")

for row in hierarchy_df.itertuples(index=False):
    indentation = "    " * int(row.level)

    print(
        f"{indentation}"
        f"{'|- ' if row.level > 0 else ''}"
        f"{row.name}"
    )


# 13. Bezposredni i posredni podwladni
section("13. WSZYSCY PODWLADNI MANAGEROW")

query_descendants = """
WITH RECURSIVE descendants AS (

    SELECT
        manager_id AS ancestor_id,
        employee_id AS descendant_id,
        1 AS depth
    FROM employees
    WHERE manager_id IS NOT NULL

    UNION ALL

    SELECT
        d.ancestor_id,
        e.employee_id,
        d.depth + 1
    FROM descendants AS d
    INNER JOIN employees AS e
        ON e.manager_id = d.descendant_id

)
SELECT
    m.employee_id AS manager_id,
    m.name AS manager,

    SUM(
        CASE WHEN d.depth = 1
        THEN 1 ELSE 0 END
    ) AS direct_subordinates,

    SUM(
        CASE WHEN d.depth > 1
        THEN 1 ELSE 0 END
    ) AS indirect_subordinates,

    COUNT(d.descendant_id) AS total_subordinates

FROM employees AS m
INNER JOIN descendants AS d
    ON m.employee_id = d.ancestor_id

GROUP BY
    m.employee_id,
    m.name

ORDER BY
    total_subordinates DESC,
    m.employee_id ASC
"""

descendants_df = pd.read_sql_query(
    query_descendants,
    conn
)

show_table(descendants_df)


# 14. Statystyki organizacyjne
section("14. STATYSTYKI ORGANIZACYJNE")

subordinates = managers_df["subordinates"].to_numpy()

stats_df = pd.DataFrame({
    "metric": [
        "Liczba pracownikow",
        "Liczba managerow z CEO",
        "Liczba pracownikow bez podwladnych",
        "Srednia liczba podwladnych",
        "Mediana liczby podwladnych",
        "Minimalna liczba podwladnych managera",
        "Maksymalna liczba podwladnych managera",
        "Liczba poziomow hierarchii"
    ],
    "value": [
        len(employees_df),
        len(managers_df),
        len(no_subordinates_df),
        np.mean(subordinates),
        np.median(subordinates),
        np.min(subordinates),
        np.max(subordinates),
        hierarchy_df["level"].max() + 1
    ]
})

show_table(stats_df.round(2))


# 15. Weryfikacja SQL za pomoca Pandas
section("15. WERYFIKACJA SQL ZA POMOCA PANDAS")

pandas_join = employees_df.merge(
    employees_df[["employee_id", "name"]],
    left_on="manager_id",
    right_on="employee_id",
    how="left",
    suffixes=("_employee", "_manager"),
    validate="many_to_one"
)

pandas_join = pandas_join.rename(columns={
    "employee_id_employee": "employee_id",
    "name_employee": "employee",
    "name_manager": "manager"
})

pandas_join = (
    pandas_join[
        ["employee_id", "employee", "manager"]
    ]
    .sort_values("employee_id")
    .reset_index(drop=True)
)

join_equal = (
    self_join_df.fillna("BRAK")
    .equals(pandas_join.fillna("BRAK"))
)

print(f"SELF JOIN SQL vs Pandas: {join_equal}")


pandas_counts = (
    employees_df
    .dropna(subset=["manager_id"])
    .groupby("manager_id")
    .size()
    .sort_index()
)

sql_counts = (
    managers_df
    .set_index("manager_id")["subordinates"]
    .sort_index()
)

counts_equal = (
    np.array_equal(
        pandas_counts.index.to_numpy(),
        sql_counts.index.to_numpy()
    )
    and np.array_equal(
        pandas_counts.to_numpy(),
        sql_counts.to_numpy()
    )
)

print(
    "Liczba podwladnych SQL vs Pandas: "
    f"{counts_equal}"
)


# 16. EXPLAIN QUERY PLAN
section("16. EXPLAIN QUERY PLAN")

plan_join_df = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_self_join,
    conn
)

print("Plan wykonania SELF JOIN:\n")

show_table(plan_join_df)


plan_managers_df = pd.read_sql_query(
    "EXPLAIN QUERY PLAN " + query_managers,
    conn
)

print("\nPlan agregacji podwladnych:\n")

show_table(plan_managers_df)


# 17. Automatyczne testy
section("17. WERYFIKACJA")

original_df = pd.read_sql_query("""
    SELECT *
    FROM employees
    ORDER BY employee_id
""", conn)

ceo_row = descendants_df.loc[
    descendants_df["manager_id"] == 1
].iloc[0]

valid_manager_ids = (
    employees_df["manager_id"]
    .dropna()
    .isin(employees_df["employee_id"])
    .all()
)

tests = {
    "Tabela zawiera 15 pracownikow":
        len(employees_df) == 15,

    "Tabela zawiera 3 kolumny":
        employees_df.shape[1] == 3,

    "Identyfikatory sa unikalne":
        employees_df["employee_id"].is_unique,

    "Nazwy pracownikow nie zawieraja NULL":
        employees_df["name"].notna().all(),

    "Wszystkie identyfikatory managerow sa poprawne":
        valid_manager_ids,

    "Brak pracownikow zarzadzajacych samym soba":
        not (
            employees_df["employee_id"]
            == employees_df["manager_id"]
        ).any(),

    "SELF JOIN zawiera 15 wierszy":
        len(self_join_df) == 15,

    "SELF JOIN zawiera 3 kolumny":
        self_join_df.shape[1] == 3,

    "SELF JOIN zachowuje wszystkich pracownikow":
        self_join_df["employee_id"].is_unique,

    "Jeden pracownik nie ma managera":
        self_join_df["manager"].isna().sum() == 1,

    "COALESCE usuwa brakujaca nazwe managera":
        coalesce_df["manager"].notna().all(),

    "TOP Management zawiera jedna osobe":
        len(top_df) == 1,

    "CEO to Anna":
        top_df.iloc[0]["name"] == "Anna",

    "Istnieje 5 managerow wraz z CEO":
        len(managers_df) == 5,

    "Kazdy manager ma podwladnych":
        managers_df["subordinates"].gt(0).all(),

    "CEO ma 4 bezposrednich podwladnych":
        ceo_row["direct_subordinates"] == 4,

    "CEO ma 10 posrednich podwladnych":
        ceo_row["indirect_subordinates"] == 10,

    "CEO ma lacznie 14 podwladnych":
        ceo_row["total_subordinates"] == 14,

    "Suma bezposrednich podwladnych wynosi 14":
        managers_df["subordinates"].sum() == 14,

    "Agregacja LEFT JOIN zawiera 15 pracownikow":
        len(all_df) == 15,

    "Dziesiec osob nie ma podwladnych":
        len(no_subordinates_df) == 10,

    "Dziesiec osob ma zero podwladnych":
        all_df["subordinates"].eq(0).sum() == 10,

    "Klasyfikacja zawiera 15 pracownikow":
        len(classification_df) == 15,

    "Klasyfikacja zawiera 3 role":
        classification_df["role"].nunique() == 3,

    "Cztery osoby maja role Manager":
        classification_df["role"].eq("Manager").sum() == 4,

    "Dziesiec osob ma role Employee":
        classification_df["role"].eq("Employee").sum() == 10,

    "Udzialy rol sumuja sie do 100 procent":
        np.isclose(roles_df["percentage"].sum(), 100),

    "INNER JOIN zawiera 14 wierszy":
        len(inner_df) == 14,

    "LEFT JOIN zawiera 15 wierszy":
        len(self_join_df) == 15,

    "INNER JOIN nie zawiera brakujacych managerow":
        inner_df["manager"].notna().all(),

    "Hierarchia zawiera wszystkich pracownikow":
        len(hierarchy_df) == 15,

    "Hierarchia zawiera unikalnych pracownikow":
        hierarchy_df["employee_id"].is_unique,

    "Hierarchia ma 3 poziomy":
        hierarchy_df["level"].nunique() == 3,

    "CEO znajduje sie na poziomie 0":
        hierarchy_df.loc[
            hierarchy_df["employee_id"] == 1,
            "level"
        ].iloc[0] == 0,

    "SELF JOIN SQL i Pandas sa zgodne":
        join_equal,

    "Liczba podwladnych SQL i Pandas jest zgodna":
        counts_equal,

    "Plan wykonania SELF JOIN nie jest pusty":
        not plan_join_df.empty,

    "Plan agregacji nie jest pusty":
        not plan_managers_df.empty,

    "Klucze obce sa poprawne":
        cursor.execute(
            "PRAGMA foreign_key_check"
        ).fetchall() == [],

    "Oryginalna tabela pozostala niezmieniona":
        employees_df.equals(original_df)
}

for description, result in tests.items():
    print(f"Czy {description}: {bool(result)}")

passed = sum(bool(result) for result in tests.values())
total = len(tests)

print(f"\nZaliczone testy: {passed}/{total}")


# 18. Wnioski
section("18. WNIOSKI")

conclusions = [
    "SELF JOIN laczy tabele z sama soba.",
    "Aliasy pozwalaja rozroznic role tej samej tabeli.",
    "manager_id wskazuje identyfikator przelozonego.",
    "Klucz obcy moze wskazywac na te sama tabele.",
    "LEFT JOIN zachowuje pracownikow bez managera.",
    "INNER JOIN pomija pracownikow bez managera.",
    "IS NULL pozwala znalezc TOP management.",
    "COALESCE pozwala zastapic brakujaca wartosc.",
    "COUNT(employee_id) liczy rzeczywistych podwladnych.",
    "GROUP BY pozwala agregowac dane wedlug managera.",
    "CASE WHEN umozliwia klasyfikacje pracownikow.",
    "SELF JOIN pozwala analizowac bezposrednie relacje.",
    "Recursive CTE pozwala analizowac wiele poziomow.",
    "CEO moze miec podwladnych bezposrednich i posrednich.",
    "Pandas merge pozwala odtworzyc operacje SELF JOIN.",
    "EXPLAIN QUERY PLAN pokazuje sposob wykonania SQL.",
    "Hierarchie organizacyjne maja zastosowanie w HR.",
    "Podobne struktury wystepuja w kategoriach produktow.",
    "Klucz obcy nie zabezpiecza przed wszystkimi cyklami.",
    "Zapytania rekurencyjne wymagaja poprawnej hierarchii."
]

for number, conclusion in enumerate(conclusions, 1):
    print(f"{number}. {conclusion}")


# 19. Podsumowanie
section("PODSUMOWANIE")

print(f"Liczba pracownikow: {len(employees_df)}")
print(f"Liczba managerow z CEO: {len(managers_df)}")
print(f"Liczba osob w TOP Management: {len(top_df)}")
print(
    "Pracownicy bez podwladnych: "
    f"{len(no_subordinates_df)}"
)
print(f"CEO: {top_df.iloc[0]['name']}")
print(
    "Bezposredni podwladni CEO: "
    f"{ceo_row['direct_subordinates']}"
)
print(
    "Posredni podwladni CEO: "
    f"{ceo_row['indirect_subordinates']}"
)
print(
    "Wszyscy podwladni CEO: "
    f"{ceo_row['total_subordinates']}"
)
print(
    "Liczba poziomow hierarchii: "
    f"{hierarchy_df['level'].max() + 1}"
)
print(f"Zaliczone testy: {passed}/{total}")

conn.close()

assert passed == total, "Nie wszystkie testy zostaly zaliczone."

print("\nWszystkie testy zakonczone pomyslnie.")
print("Zadanie 18 wykonane poprawnie.")
