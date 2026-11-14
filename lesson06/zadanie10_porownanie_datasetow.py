# Lekcja 06 - Zadanie 10: Porownanie cech dwoch datasetow

# Cechy dwoch datasetow
dataset_a = {'wiek', 'plec', 'miasto', 'dochod',
             'wyksztalcenie', 'stan_cywilny'}

dataset_b = {'wiek', 'plec', 'miasto', 'pensja',
             'stanowisko', 'staz'}

# Cechy wspolne - iloczyn zbiorow
wspolne = dataset_a & dataset_b

# Cechy tylko w datasecie A
tylko_a = dataset_a - dataset_b

# Cechy tylko w datasecie B
tylko_b = dataset_b - dataset_a

# Wszystkie unikalne cechy - suma zbiorow
wszystkie = dataset_a | dataset_b

# Roznica symetryczna
tylko_w_jednym = dataset_a ^ dataset_b

# Sprawdzenie podzbioru
czy_podzbior = {'wiek', 'plec'}.issubset(wspolne)

# Wyswietlanie wynikow
print(f"Cechy wspólne: {wspolne}")
print(f"Cechy tylko w A: {tylko_a}")
print(f"Cechy tylko w B: {tylko_b}")
print(f"Wszystkie unikalne cechy: {wszystkie}")
print(f"Cechy tylko w jednym datasecie: {tylko_w_jednym}")
print(f"Czy wiek i plec są podzbiorem cech wspólnych: {czy_podzbior}")
