import time
import os

import psutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from sklearn.ensemble import HistGradientBoostingClassifier
from xgboost import XGBClassifier
from threadpoolctl import threadpool_limits

# Lista przechowujaca wyniki wszystkich pomiarow
all_measurements = []

def measure_operation(name, operation):
    """
    Mierzy czas wykonania operacji,
    czas CPU i zmianę wykorzystania RAM.
    """

    process = psutil.Process(os.getpid())

    cpu_before = process.cpu_times()
    ram_before = process.memory_info().rss

    start = time.perf_counter()

    result = operation()

    elapsed = time.perf_counter() - start

    cpu_after = process.cpu_times()
    ram_after = process.memory_info().rss

    cpu_time = (
        cpu_after.user + cpu_after.system
        - cpu_before.user - cpu_before.system
    )

    ram_change_mb = (
        ram_after - ram_before
    ) / (1024 ** 2)

    measurement = {
        "operation": name,
        "time_seconds": elapsed,
        "cpu_seconds": cpu_time,
        "ram_change_mb": ram_change_mb,
    }

    print(f"\nOperacja: {name}")
    print(f"Czas wykonania: {elapsed:.6f} s")
    print(f"Czas CPU: {cpu_time:.6f} s")
    print(f"Zmiana RAM: {ram_change_mb:.2f} MB")

    return result, measurement

from statistics import median


def repeat_measurement(name, operation, repeats=5):
    """
    Wykonuje operacje wielokrotnie
    i oblicza mediane czasu wykonania.
    """

    measurements = []

    for i in range(repeats):
        print(f"\nPowtorzenie {i + 1}/{repeats}")

        _, measurement = measure_operation(
            name,
            operation
        )

        measurements.append(measurement)
        all_measurements.append(measurement)

    median_time = median(
        m["time_seconds"] for m in measurements
    )

    print(f"\nMediana czasu: {median_time:.6f} s")

    return median_time

def benchmark_numpy_vs_python():
    """
    Porownuje petle Pythona z operacjami NumPy.
    """

    size = 1_000_000

    data = np.arange(size, dtype=np.float64)
    python_data = data.tolist()

    print("\n=== NUMPY VS PYTHON ===")

    python_result, python_measurement = measure_operation(
        "Python - kwadraty liczb",
        lambda: [x * x for x in python_data]
    )

    numpy_result, numpy_measurement = measure_operation(
        "NumPy - kwadraty liczb",
        lambda: data * data
    )

    assert np.array_equal(python_result, numpy_result)

    print("\nWyniki obu metod sa identyczne.")

    return [python_measurement, numpy_measurement]

def benchmark_pandas():
    """
    Porownuje wektoryzacje Pandas z iterrows().
    """

    size = 100_000

    df = pd.DataFrame({
        "a": np.arange(size, dtype=np.float64),
        "b": np.arange(size, dtype=np.float64) * 2
    })

    vectorized_result = df["a"] + df["b"]

    iterrows_result = [
        row["a"] + row["b"]
        for _, row in df.iterrows()
    ]

    assert np.array_equal(
        vectorized_result.to_numpy(),
        np.array(iterrows_result)
    )

    print("\nKontrola poprawnosci Pandas: OK")

    print("\n=== PANDAS VS ITERROWS ===")

    pandas_median = repeat_measurement(
        "Pandas - wektoryzacja",
        lambda: df["a"] + df["b"],
        repeats=5
    )

    iterrows_median = repeat_measurement(
        "Pandas - iterrows",
        lambda: [
            row["a"] + row["b"]
            for _, row in df.iterrows()
        ],
        repeats=5
    )

    print("\n=== PODSUMOWANIE PANDAS ===")
    print(f"Mediana wektoryzacji: {pandas_median:.6f} s")
    print(f"Mediana iterrows:     {iterrows_median:.6f} s")
    print(
        f"Wektoryzacja szybsza: "
        f"{iterrows_median / pandas_median:.2f} razy"
    )

def create_matplotlib_chart(x, y):
    """
    Tworzy wykres liniowy Matplotlib.
    """
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.close(fig)
    return fig


def create_plotly_chart(x, y):
    """
    Tworzy wykres liniowy Plotly.
    """
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines"
        )
    )
    return fig

def benchmark_charts():
    """
    Porownuje tworzenie wykresow Matplotlib i Plotly.
    """

    x = np.linspace(0, 20, 10_000)
    y = np.sin(x)

    print("\n=== MATPLOTLIB VS PLOTLY ===")

    matplotlib_median = repeat_measurement(
        "Matplotlib - wykres liniowy",
        lambda: create_matplotlib_chart(x, y),
        repeats=5
    )

    plotly_median = repeat_measurement(
        "Plotly - wykres liniowy",
        lambda: create_plotly_chart(x, y),
        repeats=5
    )

    print("\n=== PODSUMOWANIE WYKRESOW ===")
    print(f"Mediana Matplotlib: {matplotlib_median:.6f} s")
    print(f"Mediana Plotly:     {plotly_median:.6f} s")

    if matplotlib_median < plotly_median:
        speedup = plotly_median / matplotlib_median
        print(f"Matplotlib szybszy: {speedup:.2f} razy")
    else:
        speedup = matplotlib_median / plotly_median
        print(f"Plotly szybszy: {speedup:.2f} razy")

def benchmark_machine_learning():
    """
    Porownuje trenowanie modeli Scikit-learn i XGBoost.
    """

    from sklearn.datasets import make_classification

    X, y = make_classification(
        n_samples=10_000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        random_state=42
    )

    print("\n=== SCIKIT-LEARN VS XGBOOST ===")

    sklearn_model = HistGradientBoostingClassifier(
        max_iter=100,
        learning_rate=0.1,
        random_state=42
    )

    xgboost_model = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        tree_method="hist",
        n_jobs=1,
        random_state=42
    )

    with threadpool_limits(limits=1):
        sklearn_median = repeat_measurement(
            "Scikit-learn - trenowanie",
            lambda: sklearn_model.fit(X, y),
            repeats=5
        )

    xgboost_median = repeat_measurement(
        "XGBoost - trenowanie",
        lambda: xgboost_model.fit(X, y),
        repeats=5
    )

    print("\n=== PODSUMOWANIE MACHINE LEARNING ===")
    print(f"Mediana Scikit-learn: {sklearn_median:.6f} s")
    print(f"Mediana XGBoost:      {xgboost_median:.6f} s")

def benchmark_sum():
    """
    Porownuje sumowanie liczb w Pythonie i NumPy.
    """

    data = np.arange(1_000_000, dtype=np.float64)
    python_data = data.tolist()

    print("\n=== SUMOWANIE: PYTHON VS NUMPY ===")

    python_median = repeat_measurement(
        "Python - sumowanie liczb",
        lambda: sum(python_data),
        repeats=5
    )

    numpy_median = repeat_measurement(
        "NumPy - sumowanie liczb",
        lambda: np.sum(data),
        repeats=5
    )

    assert np.isclose(
        sum(python_data),
        np.sum(data)
    )

    print("\n=== PODSUMOWANIE SUMOWANIA ===")
    print(f"Mediana Python: {python_median:.6f} s")
    print(f"Mediana NumPy:  {numpy_median:.6f} s")
    print(
        f"NumPy szybszy: "
        f"{python_median / numpy_median:.2f} razy"
    )

def benchmark_mean():
    """
    Porownuje obliczanie sredniej w Pythonie i NumPy.
    """

    data = np.arange(1_000_000, dtype=np.float64)
    python_data = data.tolist()

    print("\n=== SREDNIA: PYTHON VS NUMPY ===")

    python_median = repeat_measurement(
        "Python - srednia liczb",
        lambda: sum(python_data) / len(python_data),
        repeats=5
    )

    numpy_median = repeat_measurement(
        "NumPy - srednia liczb",
        lambda: np.mean(data),
        repeats=5
    )

    assert np.isclose(
        sum(python_data) / len(python_data),
        np.mean(data)
    )

    print("\n=== PODSUMOWANIE SREDNIEJ ===")
    print(f"Mediana Python: {python_median:.6f} s")
    print(f"Mediana NumPy:  {numpy_median:.6f} s")
    print(
        f"NumPy szybszy: "
        f"{python_median / numpy_median:.2f} razy"
    )

def benchmark_max():
    """
    Porownuje wyszukiwanie maksimum w Pythonie i NumPy.
    """

    data = np.arange(1_000_000, dtype=np.float64)
    python_data = data.tolist()

    print("\n=== MAKSIMUM: PYTHON VS NUMPY ===")

    python_median = repeat_measurement(
        "Python - maksimum",
        lambda: max(python_data),
        repeats=5
    )

    numpy_median = repeat_measurement(
        "NumPy - maksimum",
        lambda: np.max(data),
        repeats=5
    )

    assert max(python_data) == np.max(data)

    print("\n=== PODSUMOWANIE MAKSIMUM ===")
    print(f"Mediana Python: {python_median:.6f} s")
    print(f"Mediana NumPy:  {numpy_median:.6f} s")
    print(
        f"NumPy szybszy: "
        f"{python_median / numpy_median:.2f} razy"
    )

def benchmark_min():
    """
    Porownuje wyszukiwanie minimum w Pythonie i NumPy.
    """

    data = np.arange(1_000_000, dtype=np.float64)
    python_data = data.tolist()

    print("\n=== MINIMUM: PYTHON VS NUMPY ===")

    python_median = repeat_measurement(
        "Python - minimum",
        lambda: min(python_data),
        repeats=5
    )

    numpy_median = repeat_measurement(
        "NumPy - minimum",
        lambda: np.min(data),
        repeats=5
    )

    assert min(python_data) == np.min(data)

    print("\n=== PODSUMOWANIE MINIMUM ===")
    print(f"Mediana Python: {python_median:.6f} s")
    print(f"Mediana NumPy:  {numpy_median:.6f} s")
    print(
        f"NumPy szybszy: "
        f"{python_median / numpy_median:.2f} razy"
    )

def benchmark_std():
    """
    Porownuje obliczanie odchylenia standardowego.
    """

    data = np.arange(1_000_000, dtype=np.float64)
    python_data = data.tolist()

    mean_value = sum(python_data) / len(python_data)

    print("\n=== ODCHYLENIE STANDARDOWE: PYTHON VS NUMPY ===")

    python_median = repeat_measurement(
        "Python - odchylenie standardowe",
        lambda: (
            sum((x - mean_value) ** 2 for x in python_data)
            / len(python_data)
        ) ** 0.5,
        repeats=5
    )

    numpy_median = repeat_measurement(
        "NumPy - odchylenie standardowe",
        lambda: np.std(data),
        repeats=5
    )

    python_result = (
        sum((x - mean_value) ** 2 for x in python_data)
        / len(python_data)
    ) ** 0.5

    assert np.isclose(python_result, np.std(data))

    print("\n=== PODSUMOWANIE ODCHYLENIA ===")
    print(f"Mediana Python: {python_median:.6f} s")
    print(f"Mediana NumPy:  {numpy_median:.6f} s")
    print(
        f"NumPy szybszy: "
        f"{python_median / numpy_median:.2f} razy"
    )

def benchmark_filter():
    """
    Porownuje filtrowanie danych w Pythonie i NumPy.
    """

    data = np.arange(1_000_000, dtype=np.float64)
    python_data = data.tolist()
    threshold = 500_000

    print("\n=== FILTROWANIE: PYTHON VS NUMPY ===")

    python_median = repeat_measurement(
        "Python - filtrowanie",
        lambda: [x for x in python_data if x > threshold],
        repeats=5
    )

    numpy_median = repeat_measurement(
        "NumPy - filtrowanie",
        lambda: data[data > threshold],
        repeats=5
    )

    python_result = [x for x in python_data if x > threshold]
    numpy_result = data[data > threshold]

    assert np.array_equal(python_result, numpy_result)

    print("\n=== PODSUMOWANIE FILTROWANIA ===")
    print(f"Mediana Python: {python_median:.6f} s")
    print(f"Mediana NumPy:  {numpy_median:.6f} s")
    print(
        f"NumPy szybszy: "
        f"{python_median / numpy_median:.2f} razy"
    )

if __name__ == "__main__":

    size = 1_000_000
    data = np.arange(size, dtype=np.float64)
    python_data = data.tolist()

    print("\n=== PYTHON - 5 POMIAROW ===")

    python_median = repeat_measurement(
        "Python - kwadraty liczb",
        lambda: [x * x for x in python_data],
        repeats=5
    )

    print("\n=== NUMPY - 5 POMIAROW ===")

    numpy_median = repeat_measurement(
        "NumPy - kwadraty liczb",
        lambda: data * data,
        repeats=5
    )

    speedup = python_median / numpy_median

    print("\n=== PODSUMOWANIE ===")
    print(f"Mediana Python: {python_median:.6f} s")
    print(f"Mediana NumPy:  {numpy_median:.6f} s")
    print(f"NumPy szybszy: {speedup:.2f} razy")
    benchmark_pandas()
    benchmark_charts()
    benchmark_machine_learning()
    benchmark_sum()
    benchmark_mean()
    benchmark_max()
    benchmark_min()
    benchmark_std()
    benchmark_filter()

    # Zapis wszystkich pomiarow do pliku CSV
    results_df = pd.DataFrame(all_measurements)

    results_df.to_csv(
        "energy_benchmark_results.csv",
        index=False
    )

    print("\n=== ZAPIS WYNIKOW ===")
    print(f"Liczba zapisanych pomiarow: {len(results_df)}")
    print("Plik: energy_benchmark_results.csv")

    # Zbiorcze zestawienie median dla kazdej operacji
    summary_df = (
        results_df
        .groupby("operation", as_index=False)
        .agg(
            median_time_seconds=("time_seconds", "median"),
            median_cpu_seconds=("cpu_seconds", "median"),
            median_ram_change_mb=("ram_change_mb", "median")
        )
    )

    summary_df.to_csv(
        "energy_benchmark_summary.csv",
        index=False
    )

    print("\n=== ZBIORCZE WYNIKI ===")
    print(summary_df.to_string(index=False))
    print("\nPlik: energy_benchmark_summary.csv")

    # Wykres median czasu wykonania
    chart_data = summary_df.sort_values(
        "median_time_seconds",
        ascending=True
    )

    fig, ax = plt.subplots(figsize=(12, 9))

    ax.barh(
        chart_data["operation"],
        chart_data["median_time_seconds"]
    )

    ax.set_xscale("log")
    ax.set_xlabel("Mediana czasu wykonania [s] - skala logarytmiczna")
    ax.set_ylabel("Operacja")
    ax.set_title("Energy Benchmark Suite - porownanie czasu wykonania")

    ax.grid(axis="x", alpha=0.3)

    fig.tight_layout()

    fig.savefig(
        "energy_benchmark_times.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("\n=== WYKRES CZASOW ===")
    print("Zapisano: energy_benchmark_times.png")

    # Pary operacji do porownania przyspieszenia
    comparison_pairs = [
        ("Kwadraty liczb", "Python - kwadraty liczb", "NumPy - kwadraty liczb"),
        ("Pandas", "Pandas - iterrows", "Pandas - wektoryzacja"),
        ("Wykres liniowy", "Matplotlib - wykres liniowy", "Plotly - wykres liniowy"),
        ("Trenowanie ML", "Scikit-learn - trenowanie", "XGBoost - trenowanie"),
        ("Sumowanie", "Python - sumowanie liczb", "NumPy - sumowanie liczb"),
        ("Srednia", "Python - srednia liczb", "NumPy - srednia liczb"),
        ("Maksimum", "Python - maksimum", "NumPy - maksimum"),
        ("Minimum", "Python - minimum", "NumPy - minimum"),
        ("Odchylenie standardowe", "Python - odchylenie standardowe", "NumPy - odchylenie standardowe"),
        ("Filtrowanie", "Python - filtrowanie", "NumPy - filtrowanie"),
    ]

    # Obliczanie wspolczynnikow przyspieszenia
    median_times = dict(
        zip(
            summary_df["operation"],
            summary_df["median_time_seconds"]
        )
    )

    speedup_results = []

    for category, first_operation, second_operation in comparison_pairs:
        first_time = median_times[first_operation]
        second_time = median_times[second_operation]

        speedup = first_time / second_time

        speedup_results.append({
            "category": category,
            "first_operation": first_operation,
            "second_operation": second_operation,
            "speedup": speedup
        })

    speedup_df = pd.DataFrame(speedup_results)

    print("\n=== POROWNANIE PRZYSPIESZENIA ===")

    for _, row in speedup_df.iterrows():
        print(f"{row['category']}: {row['speedup']:.2f}x")

    # Wykres wspolczynnikow przyspieszenia
    speedup_chart = speedup_df.sort_values(
        "speedup",
        ascending=True
    )

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.barh(
        speedup_chart["category"],
        speedup_chart["speedup"],
        color="steelblue"
    )

    ax.set_xscale("log")
    ax.axvline(1, color="red", linestyle="--", linewidth=1)

    ax.set_xlabel("Przyspieszenie [razy] - skala logarytmiczna")
    ax.set_ylabel("Porownywana operacja")
    ax.set_title("Energy Benchmark Suite - porownanie przyspieszenia")

    ax.grid(axis="x", alpha=0.3)

    fig.tight_layout()

    fig.savefig(
        "energy_benchmark_speedup.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("\n=== WYKRES PRZYSPIESZENIA ===")
    print("Zapisano: energy_benchmark_speedup.png")

    # Zapis porownania przyspieszenia do CSV
    speedup_df.to_csv(
        "energy_benchmark_speedup.csv",
        index=False
    )

    print("\n=== ZAPIS PRZYSPIESZENIA ===")
    print(f"Liczba porownan: {len(speedup_df)}")
    print("Plik: energy_benchmark_speedup.csv")
