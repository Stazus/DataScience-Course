# Lekcja 04 - Zadanie 11: Sprawdzanie poprawności hiperparametrów

learning_rate = 0.01
batch_size = 64
epochs = 100
dropout = 0.5

# Walidacja learning_rate
if 0 < learning_rate < 1:
    print("learning_rate: OK")
else:
    print("learning_rate: BŁĄD - wartość musi być w zakresie (0, 1)")

# Walidacja batch_size
if batch_size > 0 and (batch_size & (batch_size - 1)) == 0:
    print("batch_size: OK")
else:
    print("batch_size: BŁĄD - wartość musi być potęgą liczby 2")

# Walidacja epochs
if 0 < epochs < 1000:
    print("epochs: OK")
else:
    print("epochs: BŁĄD - wartość musi być w zakresie (0, 1000)")

# Walidacja dropout
if 0 <= dropout <= 1:
    print("dropout: OK")
else:
    print("dropout: BŁĄD - wartość musi być w zakresie [0, 1]")
