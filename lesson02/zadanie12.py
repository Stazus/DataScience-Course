import matplotlib.pyplot as plt

# ==========================================
# ZADANIE 12 - GREEN IT CALCULATOR
# ==========================================

# Orientacyjna moc urządzeń w watach
DEVICE_POWER = {
    "laptop": 30,
    "desktop": 150,
    "cloud_gpu": 400
}

# Przykładowe wskaźniki emisji CO2 w g/kWh
# Wartości dydaktyczne, nie aktualne dane pomiarowe
REGION_EMISSIONS = {
    "Polska": 650,
    "Niemcy": 350,
    "Francja": 60,
    "Szwecja": 30
}

# Uproszczona emisja samochodu osobowego
CAR_EMISSION_G_PER_KM = 150

# ==========================================
# FUNKCJA OBLICZAJĄCA ŚLAD WĘGLOWY
# ==========================================

def calculate_carbon_footprint(hours, device, region):
    """
    Oblicza zużycie energii i emisję CO2 dla sesji Data Science.

    Args:
        hours: Czas pracy w godzinach.
        device: Typ urządzenia.
        region: Region określający wskaźnik emisji CO2.

    Returns:
        Słownik z wynikami obliczeń.
    """

    # Sprawdzenie poprawności danych
    if hours <= 0:
        raise ValueError("Czas pracy musi być większy od zera.")

    if device not in DEVICE_POWER:
        raise ValueError(f"Nieznane urządzenie: {device}")

    if region not in REGION_EMISSIONS:
        raise ValueError(f"Nieznany region: {region}")

    # Pobranie parametrów
    power_w = DEVICE_POWER[device]
    emission_factor = REGION_EMISSIONS[region]

    # Zużycie energii w kWh
    energy_kwh = (power_w * hours) / 1000

    # Emisja CO2 w gramach
    co2_grams = energy_kwh * emission_factor

    # Równoważna odległość przejechana samochodem
    car_distance_km = co2_grams / CAR_EMISSION_G_PER_KM

    # Wyniki
    return {
        "hours": hours,
        "device": device,
        "region": region,
        "energy_kwh": round(energy_kwh, 4),
        "co2_grams": round(co2_grams, 2),
        "car_distance_km": round(car_distance_km, 2)
    }

# ==========================================
# TEST KALKULATORA
# ==========================================

# ==========================================
# WIZUALIZACJA EMISJI CO2
# ==========================================

def create_emission_chart(hours, region):
    """Porównuje emisję CO2 trzech typów urządzeń."""

    devices = ["laptop", "desktop", "cloud_gpu"]

    emissions = [
        calculate_carbon_footprint(hours, device, region)["co2_grams"]
        for device in devices
    ]

    labels = ["Laptop", "Desktop", "Cloud GPU"]
    colors = ["seagreen", "royalblue", "darkorange"]

    plt.figure(figsize=(10, 6))

    bars = plt.bar(labels, emissions, color=colors)

    plt.title(
        f"Emisja CO2 podczas {hours} godzin pracy - {region}"
    )
    plt.xlabel("Typ urządzenia")
    plt.ylabel("Emisja CO2 (g)")

    plt.bar_label(
        bars,
        labels=[f"{value:.1f} g" for value in emissions],
        padding=3
    )

    plt.ylim(0, max(emissions) * 1.2)
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()

    plt.savefig("zadanie12_green_it.png", dpi=300)
    plt.close()

    print("\nWykres zapisano do: zadanie12_green_it.png")

if __name__ == "__main__":
    wynik = calculate_carbon_footprint(
        hours=5,
        device="laptop",
        region="Polska"
    )

    create_emission_chart(hours=5, region="Polska")

    print("\nGREEN IT CALCULATOR")
    print("=" * 40)
    print(f"Czas pracy: {wynik['hours']} godzin")
    print(f"Urządzenie: {wynik['device']}")
    print(f"Region: {wynik['region']}")
    print(f"Zużycie energii: {wynik['energy_kwh']} kWh")
    print(f"Emisja CO2: {wynik['co2_grams']} g")
    print(
        f"Odpowiednik jazdy samochodem: "
        f"{wynik['car_distance_km']} km"
    )
