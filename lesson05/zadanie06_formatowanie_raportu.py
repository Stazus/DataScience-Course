# Lekcja 05 - Zadanie 6: Formatowanie raportu

# Dane wejściowe
model_name = "XGBoost"
accuracy = 0.8934
training_time = 45.67

# Tworzenie wieloliniowego raportu za pomocą f-stringa
raport = (
    f"Model: {model_name}\n"
    f"  Accuracy: {accuracy:.2%}\n"
    f"  Training time: {training_time:.2f}s"
)

# Wyświetlenie raportu
print(raport)
