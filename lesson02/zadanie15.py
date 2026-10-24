import argparse
from pathlib import Path

import nbformat

import ast

import sys

# ==========================================
# ZADANIE 15 - COLAB-TO-LOCAL CONVERTER
# ==========================================


def remove_colab_cells(notebook):
    """
    Usuwa komórki zawierające wyłącznie
    polecenia specyficzne dla Google Colab.
    """

    cleaned_cells = []
    removed_count = 0

    for cell in notebook.cells:

        if cell.cell_type != "code":
            cleaned_cells.append(cell)
            continue

        lines = [
            line.strip()
            for line in cell.source.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

        is_colab_only = bool(lines) and all(
            line.startswith((
                "from google.colab import drive",
                "drive.mount(",
                "!pip install ",
                "%pip install "
            ))
            for line in lines
        )

        if is_colab_only:
            removed_count += 1
            continue

        cleaned_cells.append(cell)

    notebook.cells = cleaned_cells

    print(f"Usunięto komórek Colab: {removed_count}")

    return notebook

def convert_file_paths(notebook):
    """
    Zamienia ścieżki Google Drive na lokalne.
    """

    old_prefix = "/content/drive/MyDrive/"
    new_prefix = "data/"

    modified_count = 0

    for cell in notebook.cells:

        if cell.cell_type != "code":
            continue

        if old_prefix in cell.source:

            cell.source = cell.source.replace(
                old_prefix,
                new_prefix
            )

            modified_count += 1

    print(
        f"Zmieniono ścieżki w komórkach: {modified_count}"
    )

    return notebook

def detect_libraries(notebook):
    """
    Wykrywa biblioteki importowane w notebooku.
    """

    libraries = set()

    for cell in notebook.cells:

        if cell.cell_type != "code":
            continue

        try:
            tree = ast.parse(cell.source)

        except SyntaxError:
            print(
                "Pominięto komórkę z kodem "
                "niezgodnym ze składnią Pythona."
            )
            continue

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:
                    library = alias.name.split(".")[0]
                    libraries.add(library)

            elif isinstance(node, ast.ImportFrom):

                if node.module:
                    library = node.module.split(".")[0]
                    libraries.add(library)

    print("\nWykryte biblioteki:")

    for library in sorted(libraries):
        print(f" - {library}")

    return libraries

def generate_requirements(libraries, input_path):
    """
    Generuje requirements.txt na podstawie
    bibliotek wykrytych w notebooku.
    """

    package_names = {
        "sklearn": "scikit-learn",
        "PIL": "Pillow",
        "cv2": "opencv-python",
        "yaml": "PyYAML",
        "bs4": "beautifulsoup4",
    }

    standard_libraries = sys.stdlib_module_names

    requirements = set()

    for library in libraries:

        if library in standard_libraries:
            continue

        package = package_names.get(
            library,
            library
        )

        requirements.add(package)

    requirements_path = input_path.with_name(
        input_path.stem + "_requirements.txt"
    )

    requirements_path.write_text(
        "\n".join(sorted(requirements)) + "\n",
        encoding="utf-8"
    )

    print(
        f"\nWygenerowano requirements: {requirements_path}"
    )

    return requirements_path


def add_venv_instructions(notebook, requirements_path):
    """Dodaje instrukcje tworzenia srodowiska venv."""

    instructions = f"""# Przygotowanie srodowiska lokalnego

Notebook przekonwertowany z Google Colab.

## 1. Utworzenie srodowiska

    python3 -m venv venv

## 2. Aktywacja srodowiska

Linux / macOS:

    source venv/bin/activate

Windows:

    venv\\Scripts\\activate

## 3. Instalacja bibliotek

    python -m pip install -r {requirements_path.name}

## 4. Uruchomienie

Otworz notebook w Jupyter lub VS Code.
Wybierz interpreter z utworzonego srodowiska.
"""

    instruction_cell = nbformat.v4.new_markdown_cell(
        instructions
    )

    notebook.cells.insert(0, instruction_cell)

    print("Dodano instrukcje tworzenia srodowiska venv.")

    return notebook

def convert_notebook(input_path):
    """
    Wczytuje notebook Google Colab
    i przygotowuje go do konwersji lokalnej.
    """

    input_path = Path(input_path).resolve()

    if not input_path.is_file():
        raise FileNotFoundError(
            f"Nie znaleziono notebooka: {input_path}"
        )

    print("=" * 50)
    print("COLAB-TO-LOCAL CONVERTER")
    print("=" * 50)

    print(f"Notebook wejściowy: {input_path}")

    notebook = nbformat.read(
        input_path,
        as_version=4
    )

    print(f"Liczba komórek: {len(notebook.cells)}")

    notebook = convert_file_paths(notebook)

    notebook = remove_colab_cells(notebook)

    print(f"Liczba komórek po czyszczeniu: {len(notebook.cells)}")

    libraries = detect_libraries(notebook)

    requirements_path = generate_requirements(
        libraries,
        input_path
    )

    notebook = add_venv_instructions(
        notebook,
        requirements_path
    )

    for index, cell in enumerate(notebook.cells, start=1):
        print(
            f"Komórka {index}: {cell.cell_type}"
        )

    output_path = input_path.with_name(
        input_path.stem + "_local.ipynb"
    )

    nbformat.write(notebook, output_path)

    print(f"\nZapisano notebook lokalny: {output_path}")

    return notebook


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Konwersja notebooków Google Colab na lokalne"
    )

    parser.add_argument(
        "input_path",
        help="Ścieżka do notebooka Google Colab (.ipynb)"
    )

    args = parser.parse_args()

    convert_notebook(args.input_path)

