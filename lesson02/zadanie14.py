import argparse
import threading
import time
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import nbformat
import psutil
from nbclient import NotebookClient

import base64
from html import escape

# ==========================================
# ZADANIE 14 - RESOURCE-AWARE NOTEBOOK EXECUTOR
# ==========================================

def monitor_resources(stop_event, measurements, ram_threshold=80):
    """
    Monitoruje CPU i RAM w osobnym wątku.

    Args:
        stop_event: Sygnał zakończenia monitorowania.
        measurements: Lista przechowująca pomiary.
        ram_threshold: Próg ostrzegania o RAM (%).
    """

    print("\nRozpoczynam monitorowanie zasobów...")

    start_time = time.monotonic()

    # Przygotowanie pomiaru CPU
    psutil.cpu_percent(interval=None)

    while not stop_event.is_set():

        elapsed = time.monotonic() - start_time

        cpu_usage = psutil.cpu_percent(interval=None)
        ram_usage = psutil.virtual_memory().percent

        measurements.append({
            "time": elapsed,
            "cpu": cpu_usage,
            "ram": ram_usage
        })

        print(
            f"Czas: {elapsed:.1f}s | "
            f"CPU: {cpu_usage:.1f}% | "
            f"RAM: {ram_usage:.1f}%"
        )

        if ram_usage > ram_threshold:
            print(
                f"OSTRZEŻENIE! Zużycie RAM "
                f"przekroczyło {ram_threshold}%!"
            )

        # Czekamy maksymalnie sekundę.
        # Jeśli nadejdzie sygnał zakończenia,
        # przerywamy oczekiwanie natychmiast.
        stop_event.wait(1)

    print("\nMonitorowanie zasobów zakończone.")

def generate_resource_chart(measurements, output_path):
    """
    Generuje wykres zużycia CPU i RAM w czasie.
    """

    if not measurements:
        print("Brak pomiarów do wygenerowania wykresu.")
        return

    times = [item["time"] for item in measurements]
    cpu_values = [item["cpu"] for item in measurements]
    ram_values = [item["ram"] for item in measurements]

    plt.figure(figsize=(12, 6))

    plt.plot(
        times,
        cpu_values,
        label="CPU (%)",
        linewidth=2
    )

    plt.plot(
        times,
        ram_values,
        label="RAM (%)",
        linewidth=2
    )

    plt.xlabel("Czas (sekundy)")
    plt.ylabel("Zużycie zasobów (%)")
    plt.title("Monitorowanie zasobów podczas wykonywania notebooka")

    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Wykres zapisano: {output_path}")

def generate_html_report(notebook_path, measurements, chart_path):
    """
    Generuje raport HTML z wynikami monitorowania.
    """

    if not measurements:
        print("Brak pomiarów do wygenerowania raportu.")
        return

    cpu_values = [item["cpu"] for item in measurements]
    ram_values = [item["ram"] for item in measurements]

    duration = measurements[-1]["time"]

    avg_cpu = sum(cpu_values) / len(cpu_values)
    max_cpu = max(cpu_values)

    avg_ram = sum(ram_values) / len(ram_values)
    max_ram = max(ram_values)

    report_path = notebook_path.with_name(
        notebook_path.stem + "_report.html"
    )

    with open(chart_path, "rb") as image_file:
        encoded_chart = base64.b64encode(
            image_file.read()
        ).decode("ascii")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Raport monitorowania zasobów</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1100px;
                margin: 40px auto;
                padding: 20px;
                background-color: #f4f6f8;
            }}

            h1, h2 {{
                color: #243447;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
                background-color: white;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}

            th {{
                background-color: #e8eef5;
            }}

            img {{
                max-width: 100%;
                height: auto;
            }}
        </style>
    </head>

    <body>
        <h1>Raport monitorowania zasobów</h1>

        <p><strong>Notebook:</strong>
        {escape(notebook_path.name)}</p>

        <p><strong>Data raportu:</strong>
        {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <h2>Statystyki</h2>

        <table>
            <tr>
                <th>Parametr</th>
                <th>Wartość</th>
            </tr>

            <tr>
                <td>Czas monitorowania</td>
                <td>{duration:.1f} s</td>
            </tr>

            <tr>
                <td>Liczba pomiarów</td>
                <td>{len(measurements)}</td>
            </tr>

            <tr>
                <td>Średnie CPU</td>
                <td>{avg_cpu:.2f}%</td>
            </tr>

            <tr>
                <td>Maksymalne CPU</td>
                <td>{max_cpu:.2f}%</td>
            </tr>

            <tr>
                <td>Średnie RAM</td>
                <td>{avg_ram:.2f}%</td>
            </tr>

            <tr>
                <td>Maksymalne RAM</td>
                <td>{max_ram:.2f}%</td>
            </tr>
        </table>

        <h2>Wykres zużycia zasobów</h2>

        <img
            src="data:image/png;base64,{encoded_chart}"
            alt="Wykres CPU i RAM"
        >

    </body>
    </html>
    """

    report_path.write_text(
        html_content,
        encoding="utf-8"
    )

    print(f"Raport HTML zapisano: {report_path}")

def execute_notebook(notebook_path, ram_threshold=80):
    """
    Uruchamia notebook Jupyter i monitoruje
    zużycie zasobów komputera.

    Args:
        notebook_path: Ścieżka do notebooka.
        ram_threshold: Próg ostrzegania o RAM (%).
    """

    notebook_path = Path(notebook_path).resolve()

    if not notebook_path.is_file():
        raise FileNotFoundError(
            f"Nie znaleziono notebooka: {notebook_path}"
        )

    print("=" * 50)
    print("RESOURCE-AWARE NOTEBOOK EXECUTOR")
    print("=" * 50)

    print(f"Notebook: {notebook_path}")
    print(f"Próg ostrzegania RAM: {ram_threshold}%")

    # ==========================================
    # URUCHOMIENIE MONITORINGU
    # ==========================================

    stop_event = threading.Event()
    measurements = []

    monitor_thread = threading.Thread(
        target=monitor_resources,
        args=(stop_event, measurements, ram_threshold),
        daemon=True
    )

    monitor_thread.start()

    # ==========================================
    # WYKONYWANIE NOTEBOOKA
    # ==========================================

    print("\nUruchamianie notebooka Jupyter...")

    try:
        notebook = nbformat.read(
            notebook_path,
            as_version=4
        )

        client = NotebookClient(
            notebook,
            timeout=600,
            kernel_name="python3",
            resources={
                "metadata": {
                    "path": str(notebook_path.parent)
                }
            }
        )

        client.execute()

        print("\nNotebook wykonany pomyślnie.")

    finally:
        # Zatrzymujemy monitoring nawet w razie błędu
        stop_event.set()
        monitor_thread.join()

    print(f"\nLiczba zebranych pomiarów: {len(measurements)}")

    chart_path = notebook_path.with_name(
        notebook_path.stem + "_resources.png"
    )

    generate_resource_chart(
        measurements,
        chart_path
    )

    generate_html_report(
        notebook_path,
        measurements,
        chart_path
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Uruchamianie notebooków z monitoringiem zasobów"
    )

    parser.add_argument(
        "notebook_path",
        help="Ścieżka do pliku .ipynb"
    )

    parser.add_argument(
        "--ram-threshold",
        type=float,
        default=80,
        help="Próg ostrzegania o RAM w procentach (domyślnie 80)"
    )

    args = parser.parse_args()

    execute_notebook(
        notebook_path=args.notebook_path,
        ram_threshold=args.ram_threshold
    )
