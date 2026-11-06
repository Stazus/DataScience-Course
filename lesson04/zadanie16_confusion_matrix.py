# Lekcja 04 - Zadanie 16: Budowanie confusion matrix string

# Dane klasyfikacji binarnej
tp = 45
tn = 38
fp = 7
fn = 10

# Obliczenie liczby wszystkich próbek
suma = tp + tn + fp + fn

# Obliczenie metryk klasyfikacji
accuracy = (tp + tn) / suma
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1_score = 2 * (precision * recall) / (precision + recall)

# Budowanie macierzy pomyłek
print("=" * 45)
print(f"{'CONFUSION MATRIX':^45}")
print("=" * 45)

print(f"{'Predicted':>30}")
print(f"{'0':>23} {'1':>7}")
print("-" * 45)

print(f"{'Actual 0':<15} {f'[{tn}]':>8} {f'[{fp}]':>7}")
print(f"{'Actual 1':<15} {f'[{fn}]':>8} {f'[{tp}]':>7}")

print("=" * 45)

# Wyświetlenie metryk
print("\nMetryki klasyfikacji:")
print(f"{'Accuracy:':<15} {accuracy:.2%}")
print(f"{'Precision:':<15} {precision:.2%}")
print(f"{'Recall:':<15} {recall:.2%}")
print(f"{'F1-score:':<15} {f1_score:.2%}")

print(f"\nLiczba próbek: {suma}")
