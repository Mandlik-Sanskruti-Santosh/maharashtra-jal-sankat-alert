import sys
sys.path.append(r"D:\maharashtra-jal-sankat-alert\src\data")

import matplotlib.pyplot as plt
from data_loader import load_reservoirs_from_csv

def plot_district_storage(reservoirs, district_name):
    names  = [r.dam_name for r in reservoirs]
    levels = [r.current_level for r in reservoirs]
    colors = []

    for r in reservoirs:
        if r.alert_level() == "RED":
            colors.append("red")
        elif r.alert_level() == "AMBER":
            colors.append("orange")
        else:
            colors.append("green")

    plt.figure(figsize=(12, 6))
    plt.barh(names, levels, color=colors)
    plt.xlabel("Water Storage Level (%)")
    plt.title(f"{district_name} District — Dam Storage Levels")
    plt.axvline(x=25, color='red', linestyle='--', label='Critical (25%)')
    plt.axvline(x=50, color='orange', linestyle='--', label='Warning (50%)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(rf"D:\maharashtra-jal-sankat-alert\results\{district_name}_storage.png")
    plt.show()
    print(f"Chart saved!")

if __name__ == "__main__":
    CSV_PATH = r"D:\maharashtra-jal-sankat-alert\data\raw\nashik_dams.csv"
    reservoirs = load_reservoirs_from_csv(CSV_PATH)
    plot_district_storage(reservoirs, "Nashik")