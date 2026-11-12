# Lekcja 06 - Zadanie 7: Rozpakowanie rekordu

# Krotka opisująca pracownika
pracownik = ('Julia', 'Wiśniewska', 28, 'Data Analyst', 8500.0)

# Rozpakowanie wszystkich pól krotki
imie, nazwisko, wiek, stanowisko, pensja = pracownik

# Wyświetlenie danych pracownika
print(f"{imie} {nazwisko} ({wiek}) – {stanowisko}, pensja: {pensja:.2f} zł")

# Rozpakowanie z użyciem gwiazdki
imie, *reszta = pracownik

# Wyświetlenie wyników
print(f"Imię: {imie}")
print(f"Reszta: {reszta}")
