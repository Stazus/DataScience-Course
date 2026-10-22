import argparse
import subprocess
import sys
import venv
from pathlib import Path
import json

# ==========================================
# ZADANIE 13 - AUTOMATYCZNY SETUP PROJEKTU
# ==========================================

def setup_project(project_name):
    """
    Automatycznie przygotowuje nowy projekt Data Science.

    Args:
        project_name: Nazwa nowego projektu.

    Returns:
        Raport wykonanych operacji.
    """
    # ==========================================
    # TWORZENIE STRUKTURY PROJEKTU
    # ==========================================

    # Zabezpieczenie przed pustą nazwą i ścieżkami
    if not project_name or not project_name.strip():
        raise ValueError("Nazwa projektu nie może być pusta.")

    if not project_name.replace("-", "").replace("_", "").isalnum():
        raise ValueError(
            "Nazwa projektu może zawierać tylko litery, "
            "cyfry, myślniki i podkreślenia."
        )

    # Katalog główny nowego projektu
    projects_root = Path.home() / "ds_generated_projects"
    projects_root.mkdir(parents=True, exist_ok=True)

    project_path = projects_root / project_name
    # Nie nadpisujemy istniejącego projektu
    if project_path.exists():
        raise FileExistsError(
            f"Projekt '{project_name}' już istnieje."
        )

    # Lista katalogów do utworzenia
    folders = [
        "data/raw",
        "data/processed",
        "notebooks",
        "src",
        "models",
        "reports",
        "tests"
    ]

    # Tworzenie katalogów
    for folder in folders:
        folder_path = project_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)

    print(f"\nUtworzono projekt: {project_path}")
    print("\nUtworzone katalogi:")

    for folder in folders:
        print(f"  - {folder}")

    # ==========================================
    # INICJALIZACJA REPOZYTORIUM GIT
    # ==========================================

    print("\nInicjalizacja repozytorium Git...")

    subprocess.run(
        ["git", "init"],
        cwd=project_path,
        check=True,
        capture_output=True,
        text=True
    )

    print("Repozytorium Git zostało zainicjalizowane.")

    # ==========================================
    # TWORZENIE ŚRODOWISKA WIRTUALNEGO
    # ==========================================

    print("\nTworzenie środowiska wirtualnego...")

    venv_path = project_path / ".venv"

    # Tworzenie środowiska Python
    venv.EnvBuilder(with_pip=True).create(venv_path)

    # Ścieżka do Pythona w nowym środowisku
    python_venv = venv_path / "bin" / "python"

    print(f"Środowisko wirtualne utworzono: {venv_path}")

    # ==========================================
    # INSTALACJA PODSTAWOWYCH BIBLIOTEK
    # ==========================================

    packages = [
        "numpy",
        "pandas",
        "matplotlib",
        "jupyterlab"
    ]

    print("\nInstalowanie podstawowych bibliotek...")

    subprocess.run(
        [
            str(python_venv),
            "-m",
            "pip",
            "install",
            *packages
        ],
        check=True
    )

    print("Biblioteki zostały zainstalowane.")

    # ==========================================
    # GENEROWANIE JUPYTER NOTEBOOK
    # ==========================================

    print("\nTworzenie szablonu Jupyter Notebook...")

    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# Projekt Data Science: {project_name}\n",
                    "\n",
                    "## Wprowadzenie\n",
                    "Opis projektu i celów analizy."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import numpy as np\n",
                    "import pandas as pd\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "print('Środowisko Data Science gotowe!')"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    notebook_path = project_path / "notebooks" / "analysis.ipynb"

    with open(notebook_path, "w", encoding="utf-8") as file:
        json.dump(notebook, file, indent=4, ensure_ascii=False)

    print(f"Utworzono notebook: {notebook_path}")

    # ==========================================
    # GENEROWANIE README.md
    # ==========================================

    print("\nTworzenie pliku README.md...")

    readme_content = f"""# {project_name}

## Opis projektu
Projekt Data Science utworzony automatycznie.

## Struktura projektu
- data/raw/ - dane źródłowe
- data/processed/ - dane przetworzone
- notebooks/ - notebooki Jupyter
- src/ - kod źródłowy
- models/ - modele Machine Learning
- reports/ - raporty
- tests/ - testy

## Uruchomienie środowiska

```bash
source .venv/bin/activate
jupyter lab

jupyter lab
```
"""

    (project_path / "README.md").write_text(
        readme_content,
        encoding="utf-8"
    )

    # ==========================================
    # GENEROWANIE .gitignore
    # ==========================================

    print("Tworzenie pliku .gitignore...")

    gitignore_content = """# Środowisko wirtualne
.venv/

# Pliki tymczasowe Python
__pycache__/
*.pyc

# Jupyter Notebook
.ipynb_checkpoints/

# Pliki systemowe
.DS_Store
Thumbs.db

# Dane i modele
data/raw/*
data/processed/*
models/*
"""

    (project_path / ".gitignore").write_text(
        gitignore_content,
        encoding="utf-8"
    )

    print("Utworzono README.md i .gitignore.")

    # ==========================================
    # RAPORT KOŃCOWY
    # ==========================================

    print("\n" + "=" * 50)
    print("RAPORT AUTOMATYCZNEGO SETUPU PROJEKTU")
    print("=" * 50)

    print(f"Nazwa projektu: {project_name}")
    print(f"Lokalizacja: {project_path}")

    print("\nWykonane operacje:")
    print("[OK] Utworzono strukturę katalogów")
    print("[OK] Zainicjalizowano repozytorium Git")
    print("[OK] Utworzono środowisko wirtualne")
    print("[OK] Zainstalowano biblioteki Data Science")
    print("[OK] Utworzono Jupyter Notebook")
    print("[OK] Wygenerowano README.md")
    print("[OK] Wygenerowano .gitignore")

    print("\nProjekt Data Science jest gotowy!")
    print("=" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automatyczne tworzenie projektu Data Science"
    )

    parser.add_argument(
        "project_name",
        help="Nazwa nowego projektu"
    )

    args = parser.parse_args()
    setup_project(args.project_name)
