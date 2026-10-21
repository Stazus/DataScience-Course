
import matplotlib.pyplot as plt

# Dane modeli
models = [
    "Logistic Regression",
    "Random Forest",
    "ResNet50",
    "EfficientNet",
]

accuracy = [75, 85, 92, 90]
energy = [0.5, 5, 500, 50]

# Obliczenie efektywności
efficiency = [
    acc / eng for acc, eng in zip(accuracy, energy)
]

# Wyświetlenie wyników
for model, acc, eng, ratio in zip(
    models, accuracy, energy, efficiency
):
    print(
        f"{model}: accuracy={acc}%, "
        f"energia={eng} Wh, "
        f"efficiency ratio={ratio:.3f}"
    )

# Utworzenie wykresu
plt.figure(figsize=(10, 6))

for model, acc, eng in zip(models, accuracy, energy):
    plt.scatter(eng, acc, s=120)
    plt.annotate(
        model,
        (eng, acc),
        xytext=(8, 8),
        textcoords="offset points",
    )

plt.xscale("log")
plt.xlabel("Zużycie energii (Wh) - skala logarytmiczna")
plt.ylabel("Dokładność (accuracy, %)")
plt.title("Trade-off: dokładność vs zużycie energii")
plt.grid(True, alpha=0.3)
plt.ylim(70, 100)
plt.tight_layout()

plt.savefig("zadanie10_wykres.png", dpi=150)
plt.close()

print("\nZapisano wykres: zadanie10_wykres.png")
