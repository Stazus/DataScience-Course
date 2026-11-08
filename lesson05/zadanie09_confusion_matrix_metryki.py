# Lekcja 05 - Zadanie 9: Confusion matrix i metryki

# Macierz pomyłek
cm = [
    [80, 10],  # TN, FP
    [5, 45]    # FN, TP
]

# Wyodrębnienie wartości przez indeksowanie
TN = cm[0][0]
FP = cm[0][1]
FN = cm[1][0]
TP = cm[1][1]

# Obliczanie metryk
accuracy = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP)
recall = TP / (TP + FN)

# Wyświetlanie wyników
print(f"TN: {TN}, FP: {FP}, FN: {FN}, TP: {TP}")
print(f"Accuracy: {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
