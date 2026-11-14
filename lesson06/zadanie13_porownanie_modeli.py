# Lekcja 06 - Zadanie 13: Porownanie trzech modeli w formie tabeli

# Wyniki modeli Machine Learning
wyniki = {
    'LogReg': {
        'acc': 0.9667, 'prec': 0.9673,
        'rec': 0.9667, 'f1': 0.9667
    },
    'DecisionTree': {
        'acc': 0.9333, 'prec': 0.9342,
        'rec': 0.9333, 'f1': 0.9332
    },
    'RandomForest': {
        'acc': 0.9600, 'prec': 0.9610,
        'rec': 0.9600, 'f1': 0.9601
    }
}

# Posortowane nazwy modeli
modele = sorted(wyniki.keys())

# Obliczenie sredniej accuracy
srednia_acc = (
    wyniki['LogReg']['acc']
    + wyniki['DecisionTree']['acc']
    + wyniki['RandomForest']['acc']
) / 3

# Obliczenie sredniej F1
srednia_f1 = (
    wyniki['LogReg']['f1']
    + wyniki['DecisionTree']['f1']
    + wyniki['RandomForest']['f1']
) / 3

# Naglowek tabeli
print("=" * 60)
print(f"{'Model':<16}{'Acc':<8}{'Prec':<8}{'Rec':<8}{'F1':<8}")
print("=" * 60)

# Wyniki modelu Logistic Regression
print(
    f"{modele[1]:<16}"
    f"{wyniki['LogReg']['acc']:<8.4f}"
    f"{wyniki['LogReg']['prec']:<8.4f}"
    f"{wyniki['LogReg']['rec']:<8.4f}"
    f"{wyniki['LogReg']['f1']:<8.4f}"
)

# Wyniki modelu Decision Tree
print(
    f"{modele[0]:<16}"
    f"{wyniki['DecisionTree']['acc']:<8.4f}"
    f"{wyniki['DecisionTree']['prec']:<8.4f}"
    f"{wyniki['DecisionTree']['rec']:<8.4f}"
    f"{wyniki['DecisionTree']['f1']:<8.4f}"
)

# Wyniki modelu Random Forest
print(
    f"{modele[2]:<16}"
    f"{wyniki['RandomForest']['acc']:<8.4f}"
    f"{wyniki['RandomForest']['prec']:<8.4f}"
    f"{wyniki['RandomForest']['rec']:<8.4f}"
    f"{wyniki['RandomForest']['f1']:<8.4f}"
)

# Podsumowanie
print("=" * 60)
print(f"Srednia acc: {srednia_acc:.4f}")
print(f"Srednia f1 : {srednia_f1:.4f}")
