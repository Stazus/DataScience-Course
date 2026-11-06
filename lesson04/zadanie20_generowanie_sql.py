# Lekcja 04 - Zadanie 20: Generowanie SQL query z Python

# Dane wejściowe
tabela = "patients"
kolumny = ["patient_id", "age", "diagnosis"]

minimalny_wiek = 40
diagnozy = ["diabetes", "hypertension"]

sortowanie = "age"
limit = 100

# Łączenie nazw kolumn
kolumny_sql = ", ".join(kolumny)

# Przygotowanie listy diagnoz do SQL
diagnozy_sql = ", ".join(f"'{diagnoza}'" for diagnoza in diagnozy)

# Generowanie zapytania SQL
zapytanie_sql = (
    f"SELECT {kolumny_sql}\n"
    f"FROM {tabela}\n"
    f"WHERE age > {minimalny_wiek} "
    f"AND diagnosis IN ({diagnozy_sql})\n"
    f"ORDER BY {sortowanie} DESC\n"
    f"LIMIT {limit};"
)

# Wyświetlenie zapytania
print(zapytanie_sql)
