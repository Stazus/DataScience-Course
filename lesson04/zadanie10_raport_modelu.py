# Lekcja 04 - Zadanie 10: Budowanie raportu modelu

# Dane modelu
nazwa_modelu = "XGBoost Classifier"
dataset = "Credit Card Fraud"
liczba_probek = 284807

accuracy = 0.9991
precision = 0.8876
recall = 0.7561

# Obliczenie F1-Score
f1_score = 2 * (precision * recall) / (precision + recall)

# Szerokość raportu
szerokosc = 50

# Budowanie raportu
print("=" * szerokosc)
print(f"{'RAPORT WYNIKÓW MODELU':^{szerokosc}}")
print("=" * szerokosc)

print(f"{'Model:':<20} {nazwa_modelu}")
print(f"{'Dataset:':<20} {dataset}")
print(f"{'Liczba próbek:':<20} {liczba_probek:,}")

print("-" * szerokosc)

print(f"{'Accuracy:':<20} {accuracy:.2%}")
print(f"{'Precision:':<20} {precision:.2%}")
print(f"{'Recall:':<20} {recall:.2%}")
print(f"{'F1-Score:':<20} {f1_score:.2%}")

print("=" * szerokosc)
