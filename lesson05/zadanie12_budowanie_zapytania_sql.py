# Lekcja 05 - Zadanie 12: Budowanie zapytania SQL

# Dane wejściowe
tabela = "customers"
kolumny = ['id', 'name', 'email', 'city']
warunek = "city = 'New York'"

# Łączenie nazw kolumn
kolumny_sql = ", ".join(kolumny)

# Budowanie zapytania za pomocą f-stringa
zapytanie_sql = f"SELECT {kolumny_sql} FROM {tabela} WHERE {warunek}"

# Wyświetlanie wyników
print(f"Tabela: {tabela}")
print(f"Kolumny: {kolumny_sql}")
print(f"Warunek: {warunek}")
print(f"Zapytanie SQL: {zapytanie_sql}")
