from pathlib import Path
from time import perf_counter
import json
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent
NOTEBOOK = BASE_DIR / "test_notebook.ipynb"

ENVIRONMENTS = {
    "Local Python 3.9": BASE_DIR / "venv39/bin/python",
    "Local Python 3.11": BASE_DIR / "venv311/bin/python",
}


def run_notebook(name, python_path):
    print(f"\nUruchamianie: {name}")

    output_path = BASE_DIR / (
        f"result_{name.lower().replace(' ', '_').replace('.', '')}.json"
    )

    script = """
import json
import sys
import nbformat
from nbclient import NotebookClient

notebook = nbformat.read(sys.argv[1], as_version=4)

client = NotebookClient(
    notebook,
    timeout=120,
    kernel_name="python3",
)

client.execute()

outputs = []

for cell in notebook.cells:
    for output in cell.get("outputs", []):
        if output.output_type == "stream":
            outputs.append(output.text)
        elif output.output_type == "error":
            raise RuntimeError(output.evalue)

with open(sys.argv[2], "w", encoding="utf-8") as file:
    json.dump(
        {"python": sys.version.split()[0], "outputs": outputs},
        file,
        indent=2,
        ensure_ascii=False,
    )
"""

    start = perf_counter()

    subprocess.run(
        [
            str(python_path),
            "-c",
            script,
            str(NOTEBOOK),
            str(output_path),
        ],
        check=True,
    )

    elapsed = perf_counter() - start

    data = json.loads(output_path.read_text(encoding="utf-8"))
    data["elapsed_seconds"] = round(elapsed, 3)

    print(f"Python: {data['python']}")
    print(f"Czas wykonania: {elapsed:.3f} s")

    return data

def run_docker():
    name = "Docker Python 3.11"
    print(f"\nUruchamianie: {name}")

    output_path = BASE_DIR / "result_docker_python311.json"

    script = """
import json
import sys
import nbformat
from nbclient import NotebookClient

notebook = nbformat.read(
    "/app/test_notebook.ipynb",
    as_version=4,
)

client = NotebookClient(
    notebook,
    timeout=120,
    kernel_name="python3",
)

client.execute()

outputs = []

for cell in notebook.cells:
    for output in cell.get("outputs", []):
        if output.output_type == "stream":
            outputs.append(output.text)
        elif output.output_type == "error":
            raise RuntimeError(output.evalue)

with open("/app/result_docker_python311.json", "w", encoding="utf-8") as file:
    json.dump(
        {"python": sys.version.split()[0], "outputs": outputs},
        file,
        indent=2,
        ensure_ascii=False,
    )
"""

    start = perf_counter()

    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{BASE_DIR}:/app",
            "zadanie18-tester:python311",
            "python",
            "-c",
            script,
        ],
        check=True,
    )

    elapsed = perf_counter() - start

    data = json.loads(output_path.read_text(encoding="utf-8"))
    data["elapsed_seconds"] = round(elapsed, 3)

    print(f"Python: {data['python']}")
    print(f"Czas wykonania: {elapsed:.3f} s")

    return data

def run_colab():
    name = "Google Colab"
    print(f"\nOdczytywanie wyników: {name}")

    import nbformat

    notebook_path = BASE_DIR / "test_notebook_colab.ipynb"
    notebook = nbformat.read(notebook_path, as_version=4)

    outputs = []

    for cell in notebook.cells:
        for output in cell.get("outputs", []):
            if output.output_type == "stream":
                outputs.append(output.text)
            elif output.output_type == "error":
                raise RuntimeError(output.evalue)

    if len(outputs) != 4:
        raise ValueError(
            f"Nieprawidłowa liczba wyników Colab: {len(outputs)}"
        )

    python_version = outputs[0].splitlines()[0].split(":", 1)[1].strip()

    time_line = outputs[3].strip()
    if not time_line.startswith("Czas wykonania Colab: "):
        raise ValueError("Brak prawidłowego pomiaru czasu Colab")

    elapsed = float(
        time_line.split(":", 1)[1].strip().split()[0]
    )

    data = {
        "python": python_version,
        "outputs": outputs[:3],
        "elapsed_seconds": elapsed,
    }

    print(f"Python: {data['python']}")
    print(f"Czas wykonania: {elapsed:.3f} s")

    return data

def generate_report(results):
    report_path = BASE_DIR / "raport_zadanie18.md"

    lines = [
        "# Zadanie 18 – Multi-environment tester",
        "",
        "## 1. Porównanie środowisk",
        "",
        "| Środowisko | Python | Czas wykonania |",
        "|---|---|---:|",
    ]

    for name, data in results.items():
        elapsed = data["elapsed_seconds"]

        if elapsed is None:
            time_text = "Brak pomiaru"
        else:
            time_text = f"{elapsed:.3f} s"

        lines.append(
            f"| {name} | {data['python']} | {time_text} |"
        )


    lines.extend([
        "",
        "## 2. Porównanie wyników obliczeń",
        "",
    ])

    names = list(results)
    reference = results[names[0]]["outputs"][1:]

    for name in names[1:]:
        current = results[name]["outputs"][1:]
        identical = current == reference

        status = "IDENTYCZNE" if identical else "RÓŻNE"

        lines.append(f"- {names[0]} vs {name}: **{status}**")

        if not identical:
            for index in range(max(len(reference), len(current))):
                expected = (
                    reference[index].strip()
                    if index < len(reference)
                    else "<brak wyniku>"
                )
                actual = (
                    current[index].strip()
                    if index < len(current)
                    else "<brak wyniku>"
                )

                if expected != actual:
                    lines.append(
                        f"  - Różnica w wyniku {index + 1}: "
                        f"oczekiwano `{expected}`, otrzymano `{actual}`"
                    )

    lines.extend([
        "",
        "## 3. Uwagi",
        "",
        "- Porównywane są wyniki obliczeń, bez informacji o środowisku.",
        "- Local Python 3.9, Local Python 3.11 i Docker: "
        "czas obejmuje uruchomienie procesu, kernela Jupyter "
        "oraz wykonanie notebooka.",
        "- Google Colab: czas zmierzono wewnątrz notebooka "
        "za pomocą time.perf_counter().",
        "- Czasy Google Colab i pozostałych środowisk "
        "nie są bezpośrednio porównywalne.",
        "- Testy lokalne i Docker uruchamiane są automatycznie.",
        "- Google Colab uruchamiany jest ręcznie, "
        "a zapisane wyniki są automatycznie porównywane.",
        "- Wyniki czasu mogą zależeć od obciążenia komputera.",
        "",
    ])

    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"\nRaport zapisano: {report_path}")

def main():
    results = {}

    for name, python_path in ENVIRONMENTS.items():
        results[name] = run_notebook(name, python_path)

    results["Docker Python 3.11"] = run_docker()
    results["Google Colab"] = run_colab()

    print("\nPorównanie wyników:")

    names = list(results)

    reference = results[names[0]]["outputs"][1:]

    for name in names[1:]:
        current = results[name]["outputs"][1:]

        identical = current == reference

        status = "IDENTYCZNE" if identical else "RÓŻNE"

        print(f"{names[0]} vs {name}: {status}")

        if not identical:
            for index in range(max(len(reference), len(current))):
                expected = (
                    reference[index].strip()
                    if index < len(reference)
                    else "<brak wyniku>"
                )

                actual = (
                    current[index].strip()
                    if index < len(current)
                    else "<brak wyniku>"
                )

                if expected != actual:
                    print(f"  Różnica w wyniku {index + 1}")
                    print(f"  Oczekiwano: {expected}")
                    print(f"  Otrzymano: {actual}")

    generate_report(results)

if __name__ == "__main__":
    main()
