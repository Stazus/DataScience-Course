# Lekcja 05 - Zadanie 11: Parsowanie linii logu

# Dane wejściowe
log = "2024-01-15 10:23:45 ERROR Training failed due to OOM"

# Podział logu na cztery elementy
elementy = log.split(" ", 3)

# Wyodrębnienie poszczególnych pól
data = elementy[0]
czas = elementy[1]
poziom = elementy[2]
wiadomosc = elementy[3]

# Sprawdzenie, czy poziom logowania jest znany
znane_poziomy = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
poziom_znany = poziom in znane_poziomy

# Wyświetlanie wyników
print(f"Elementy logu: {elementy}")
print(f"[{data} {czas}] {poziom}: {wiadomosc}")
print(f"Czy poziom logowania jest znany: {poziom_znany}")
