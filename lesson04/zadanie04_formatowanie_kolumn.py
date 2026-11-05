# Lekcja 04 - Zadanie 4: Formatowanie nazw kolumn

nazwa_kolumny = " PATIENT_age_YEARS "

nazwa_kolumny = nazwa_kolumny.strip()
nazwa_kolumny = nazwa_kolumny.lower()
nazwa_kolumny = nazwa_kolumny.replace("_", " ")
nazwa_kolumny = nazwa_kolumny.title()

print(nazwa_kolumny)
