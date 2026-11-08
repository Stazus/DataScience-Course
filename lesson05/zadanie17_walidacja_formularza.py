# Lekcja 05 - Zadanie 17: Walidacja wartości z formularza

# Dane wejściowe
pole_imie = "  Alice  "
pole_wiek = "  28  "
pole_email = "  alice@EXAMPLE.com  "

# Czyszczenie danych
pole_imie_czyste = pole_imie.strip()
pole_wiek_czyste = pole_wiek.strip()
pole_email_czyste = pole_email.strip().lower()

# Walidacja poszczególnych pól
czy_imie_ok = pole_imie_czyste.isalpha()
czy_wiek_ok = pole_wiek_czyste.isdigit()
czy_email_ok = '@' in pole_email_czyste

# Zbiorczy wynik walidacji
wszystkie_ok = czy_imie_ok and czy_wiek_ok and czy_email_ok

# Wyświetlanie oczyszczonych danych
print("DANE PO OCZYSZCZENIU")
print(f"Imię: {pole_imie_czyste}")
print(f"Wiek: {pole_wiek_czyste}")
print(f"Email: {pole_email_czyste}")

# Wyświetlanie wyników walidacji
print("\nWALIDACJA")
print(f"Imię poprawne: {czy_imie_ok}")
print(f"Wiek poprawny: {czy_wiek_ok}")
print(f"Email poprawny: {czy_email_ok}")
print(f"Wszystkie pola OK? {wszystkie_ok}")
