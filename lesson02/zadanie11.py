import json
import os
import sys
import platform
import subprocess
from datetime import datetime
from pathlib import Path

import psutil


# ==========================================
# ZADANIE 11 - AUTOMATYCZNY RAPORT ŚRODOWISKA
# ==========================================

def generate_environment_report(output_dir="reports"):
    """
    Generuje raport środowiska Python i zasobów komputera.

    Args:
        output_dir: Katalog, w którym zostanie zapisany raport.

    Returns:
        Ścieżka do zapisanego pliku JSON.
    """
    # Aktualna data i godzina
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    # Informacje o zainstalowanych bibliotekach
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=json"],
        capture_output=True,
        text=True,
        check=True
    )

    biblioteki = json.loads(result.stdout)

    # Informacje o środowisku Python i systemie
    raport = {
        "timestamp": timestamp,
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "operating_system": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "installed_libraries_count": len(biblioteki),
        "installed_libraries": biblioteki
    }

    print("Informacje o środowisku zostały zebrane.")
    print(f"Wersja Python: {raport['python_version']}")
    print(f"System operacyjny: {raport['operating_system']}")
    print(f"Liczba bibliotek: {raport['installed_libraries_count']}")

    # ==========================================
    # INFORMACJE O CPU
    # ==========================================

    raport["cpu_physical_cores"] = psutil.cpu_count(logical=False)
    raport["cpu_logical_cores"] = psutil.cpu_count(logical=True)
    raport["cpu_usage_percent"] = psutil.cpu_percent(interval=1)

    # ==========================================
    # INFORMACJE O RAM
    # ==========================================

    pamiec = psutil.virtual_memory()

    raport["ram_total_gb"] = round(
        pamiec.total / (1024 ** 3), 2
    )

    raport["ram_available_gb"] = round(
        pamiec.available / (1024 ** 3), 2
    )

    raport["ram_usage_percent"] = pamiec.percent

    print("\nInformacje o zasobach:")
    print(f"Rdzenie fizyczne CPU: {raport['cpu_physical_cores']}")
    print(f"Procesory logiczne CPU: {raport['cpu_logical_cores']}")
    print(f"Obciążenie CPU: {raport['cpu_usage_percent']}%")
    print(f"Całkowita pamięć RAM: {raport['ram_total_gb']} GB")
    print(f"Dostępna pamięć RAM: {raport['ram_available_gb']} GB")
    print(f"Wykorzystanie RAM: {raport['ram_usage_percent']}%")

    # ==========================================
    # INFORMACJE O GPU
    # ==========================================

    raport["gpu_available"] = False
    raport["gpu_info"] = []

    try:
        wynik_gpu = subprocess.run(
            [
                "/usr/lib/wsl/lib/nvidia-smi",
                "--query-gpu=name,memory.total,driver_version",
                "--format=csv,noheader,nounits"
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )

        for linia in wynik_gpu.stdout.strip().splitlines():
            nazwa, pamiec_mb, sterownik = [
                element.strip() for element in linia.split(",", 2)
            ]

            raport["gpu_info"].append({
                "name": nazwa,
                "memory_total_mb": float(pamiec_mb),
                "driver_version": sterownik
            })

        raport["gpu_available"] = bool(raport["gpu_info"])

    except (subprocess.SubprocessError, OSError, ValueError):
        print("\nNie udało się odczytać informacji o GPU.")

    print("\nInformacje o GPU:")
    print(f"GPU dostępne: {raport['gpu_available']}")
    print(f"Szczegóły GPU: {raport['gpu_info']}")

    # ==========================================
    # ZAPIS RAPORTU DO PLIKU JSON
    # ==========================================

    # Utworzenie katalogu, jeśli nie istnieje
    katalog = Path(output_dir)
    katalog.mkdir(parents=True, exist_ok=True)

    # Nazwa pliku zawierająca datę i godzinę
    nazwa_pliku = datetime.now().strftime(
        "environment_report_%Y%m%d_%H%M%S_%f.json"
    )

    sciezka_pliku = katalog / nazwa_pliku

    # Zapis raportu do JSON
    with open(sciezka_pliku, "w", encoding="utf-8") as plik:
        json.dump(raport, plik, indent=4, ensure_ascii=False)

    print(f"\nRaport zapisano do: {sciezka_pliku}")

    # Zwrócenie ścieżki zapisanego pliku
    return str(sciezka_pliku)


# ==========================================
# URUCHOMIENIE PROGRAMU
# ==========================================

if __name__ == "__main__":
    sciezka = generate_environment_report(output_dir="reports")
    print(f"\nFunkcja zwróciła ścieżkę: {sciezka}")
