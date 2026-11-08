# Lekcja 05 - Zadanie 10: Łączenie i dzielenie listy

# Lista nazw modeli
modele = ['LogisticRegression', 'RandomForest', 'XGBoost', 'SVM']

# Łączenie elementów listy w string
modele_string = ", ".join(modele)

# Budowanie zapytania SQL za pomocą f-stringa
zapytanie_sql = f"SELECT model FROM ({modele_string})"

# Ponowny podział stringa na listę
modele_odtworzone = modele_string.split(", ")

# Porównanie list
czy_identyczne = modele == modele_odtworzone

# Wyświetlanie wyników
print(f"Lista oryginalna: {modele}")
print(f"Połączony string: {modele_string}")
print(f"Zapytanie SQL: {zapytanie_sql}")
print(f"Lista po split: {modele_odtworzone}")
print(f"Czy listy są identyczne: {czy_identyczne}")
