import csv
import sys
sys.path.append(r"D:\maharashtra-jal-sankat-alert\src\data")

from reservoir import Reservoir
from district import District


def load_reservoirs_from_csv(filepath):
    """
    Load reservoirs from a single district CSV file.
    Returns a list of Reservoir objects.
    """
    reservoirs = []

    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reservoir = Reservoir(
                dam_name             = row['dam_name'],
                district             = row['district'],
                total_capacity       = float(row['total_capacity_mcft']),
                current_level        = float(row['current_level_pct']),
                daily_depletion_rate = float(row['daily_depletion_rate'])
            )
            reservoirs.append(reservoir)

    return reservoirs


def load_all_districts(filepath):
    """
    Load ALL Maharashtra districts from master CSV file.
    Returns a list of District objects — each containing
    their Reservoir objects already added.
    """
    districts = {}  # district_name → District object

    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            district_name = row['district']

            # if district not seen before — create it
            if district_name not in districts:
                districts[district_name] = District(
                    name                   = row['district'],
                    population             = int(row['population']),
                    avg_annual_rainfall_mm = int(row['avg_rainfall_mm']),
                    daily_water_demand_mcft= int(row['daily_demand_mcft']),
                    drought_prone_talukas  = row['drought_prone_talukas'].split(',')
                )

            # create reservoir and add to district
            reservoir = Reservoir(
                dam_name             = row['dam_name'],
                district             = row['district'],
                total_capacity       = float(row['total_capacity_mcft']),
                current_level        = float(row['current_level_pct']),
                daily_depletion_rate = float(row['daily_depletion_rate'])
            )
            districts[district_name].add_reservoir(reservoir)

    return list(districts.values())


# ── Test ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    MASTER_CSV = r"D:\maharashtra-jal-sankat-alert\data\raw\maharashtra_all_districts.csv"

    print("=" * 60)
    print("  TEST 1 — Load ALL districts")
    print("=" * 60)
    all_districts = load_all_districts(MASTER_CSV)
    print(f"Loaded {len(all_districts)} districts\n")
    for d in sorted(all_districts, key=lambda x: x.average_storage_percent()):
        print(f"  {d}")

    print("\n--- CRITICAL DISTRICTS (RED) ---")
    for d in all_districts:
        if d.district_alert_level() == "RED":
            print(f"  🔴 {d.name} — {d.average_storage_percent()}%")

    print("\n--- AMBER DISTRICTS ---")
    for d in all_districts:
        if d.district_alert_level() == "AMBER":
            print(f"  🟡 {d.name} — {d.average_storage_percent()}%")

    print("\n--- SAFE DISTRICTS (GREEN) ---")
    for d in all_districts:
        if d.district_alert_level() == "GREEN":
            print(f"  🟢 {d.name} — {d.average_storage_percent()}%")