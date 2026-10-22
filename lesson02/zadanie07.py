import os
import time

import numpy as np
import psutil


# ==========================================
# ZADANIE 7 - MONITORING ZASOBÓW
# ==========================================

# Monitorowany proces Pythona
proces = psutil.Process(os.getpid())

# 1. Pomiar przed obliczeniami
cpu_przed = psutil.cpu_percent(interval=1)
ram_przed = proces.memory_info().rss / (1024 ** 2)

print("=== PRZED OBLICZENIAMI ===")
print(f"Zużycie CPU: {cpu_przed:.2f}%")
print(f"Pamięć RAM procesu: {ram_przed:.2f} MB")

# 2. Tworzenie macierzy 1000 x 1000
print("\nTworzenie macierzy 1000 x 1000...")

np.random.seed(42)
macierz = np.random.rand(1000, 1000)

# 3. Obliczenie macierzy odwrotnej
print("Obliczanie macierzy odwrotnej...")

start = time.perf_counter()

macierz_odwrotna = np.linalg.inv(macierz)

czas_obliczen = time.perf_counter() - start

# 4. Pomiar po obliczeniach
cpu_po = psutil.cpu_percent(interval=1)
ram_po = proces.memory_info().rss / (1024 ** 2)

# 5. Raport
print("\n=== RAPORT ZUŻYCIA ZASOBÓW ===")
print(f"CPU przed: {cpu_przed:.2f}%")
print(f"CPU po: {cpu_po:.2f}%")
print(f"RAM przed: {ram_przed:.2f} MB")
print(f"RAM po: {ram_po:.2f} MB")
print(f"Różnica RAM: {ram_po - ram_przed:+.2f} MB")
print(f"Czas obliczeń: {czas_obliczen:.2f} s")
