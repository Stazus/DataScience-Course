
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

# Zadanie 17 – Benchmark: Energy vs Accuracy
# Wszystkie wartości są hipotetyczne.
# Nie pochodzą z rzeczywistych pomiarów modeli.

models = [
    "Keyword Matching",
    "Logistic Regression",
    "Random Forest",
    "LSTM",
    "BERT",
]

accuracy = [70, 84, 82, 87, 92]

# Energia inferencji na 1000 predykcji (Wh)
energy = [0.02, 0.05, 0.40, 2.00, 5.00]

plt.figure(figsize=(12, 7))

plt.scatter(
    energy,
    accuracy,
    s=160,
    zorder=3,
)

for model, x, y in zip(models, energy, accuracy):
    plt.annotate(
        model,
        (x, y),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=10,
    )

plt.xscale("log")

plt.xlabel("Energia na 1000 predykcji (Wh)")
plt.ylabel("Accuracy (%)")

plt.title(
    "Benchmark klasyfikacji tekstu – Accuracy vs Energy\n"
    "Wartości hipotetyczne, nie wyniki eksperymentów"
)

plt.grid(
    True,
    which="both",
    linestyle="--",
    alpha=0.4,
)

plt.ylim(65, 96)
plt.tight_layout()

plt.savefig(
    "zadanie17_wykres.png",
    dpi=200,
    bbox_inches="tight",
)

plt.close()

print("Wykres zapisano: zadanie17_wykres.png")
