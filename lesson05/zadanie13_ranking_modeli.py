# Lekcja 05 - Zadanie 13: Ranking modeli bez pętli

# Modele i ich accuracy
m1 = ['LogisticRegression', 0.78]
m2 = ['RandomForest', 0.92]
m3 = ['SVM', 0.85]
m4 = ['XGBoost', 0.95]

# Lista wszystkich modeli
wszystkie = [m1, m2, m3, m4]

# Wyodrębnienie wartości accuracy
accuracy = [m1[1], m2[1], m3[1], m4[1]]

# Sortowanie accuracy malejąco
accuracy.sort(reverse=True)

# Trzy najlepsze wartości
top_3 = accuracy[:3]

# Najwyższa i najniższa accuracy
maksimum = max(accuracy)
minimum = min(accuracy)

# Wyświetlanie wyników
print(f"Wszystkie modele: {wszystkie}")
print(f"Accuracy malejąco: {accuracy}")
print(f"Top 3 accuracy: {top_3}")
print(f"Najwyższa accuracy: {maksimum:.2%}")
print(f"Najniższa accuracy: {minimum:.2%}")
