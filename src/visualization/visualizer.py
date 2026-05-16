import sys
sys.path.append(r"D:\maharashtra-jal-sankat-alert\src\data")

import matplotlib.pyplot as plt
from data_loader import load_reservoirs_from_csv, load_all_districts


def plot_district_storage(reservoirs, district_name):
    """
    Plot water storage levels for a single district.
    Bars are color coded — RED, AMBER, GREEN.
    """
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
    print(f"Chart saved — {district_name}_storage.png")


def plot_all_districts(all_districts):
    """
    Plot water storage levels for ALL Maharashtra districts.
    Sorted from most critical to safest.
    Color coded — RED, AMBER, GREEN.
    """
    names  = [d.name for d in all_districts]
    levels = [d.average_storage_percent() for d in all_districts]
    colors = []

    for d in all_districts:
        if d.district_alert_level() == "RED":
            colors.append("red")
        elif d.district_alert_level() == "AMBER":
            colors.append("orange")
        else:
            colors.append("green")

    # sort by level — most critical at top
    sorted_data = sorted(zip(levels, names, colors))
    levels, names, colors = zip(*sorted_data)

    plt.figure(figsize=(14, 16))
    plt.barh(names, levels, color=colors)
    plt.xlabel("Water Storage Level (%)")
    plt.title("Maharashtra Jal Sankat Alert — All Districts Water Storage")
    plt.axvline(x=25, color='red', linestyle='--', linewidth=2, label='Critical threshold (25%)')
    plt.axvline(x=50, color='orange', linestyle='--', linewidth=2, label='Warning threshold (50%)')

    # add percentage labels on each bar
    for i, (level, name) in enumerate(zip(levels, names)):
        plt.text(level + 0.5, i, f"{level}%", va='center', fontsize=8)

    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(rf"D:\maharashtra-jal-sankat-alert\results\all_districts_storage.png",
                dpi=150, bbox_inches='tight')
    plt.show()
    print("All districts chart saved — all_districts_storage.png")


def print_district_summary(all_districts):
    """
    Print a quick text summary of all districts by alert level.
    """
    red    = [d for d in all_districts if d.district_alert_level() == "RED"]
    amber  = [d for d in all_districts if d.district_alert_level() == "AMBER"]
    green  = [d for d in all_districts if d.district_alert_level() == "GREEN"]

    print("\n" + "=" * 55)
    print("  MAHARASHTRA JAL SANKAT ALERT — STATE SUMMARY")
    print("=" * 55)
    print(f"  Total districts analysed : {len(all_districts)}")
    print(f"  🔴 RED   (Critical)      : {len(red)} districts")
    print(f"  🟡 AMBER (Warning)       : {len(amber)} districts")
    print(f"  🟢 GREEN (Safe)          : {len(green)} districts")
    print("=" * 55)

    if red:
        print("\n  🔴 CRITICAL — Immediate attention needed:")
        for d in sorted(red, key=lambda x: x.average_storage_percent()):
            print(f"     {d.name:20} {d.average_storage_percent()}% — {d.days_of_water_remaining()} days remaining")

    if amber:
        print("\n  🟡 AMBER — Monitor closely:")
        for d in sorted(amber, key=lambda x: x.average_storage_percent()):
            print(f"     {d.name:20} {d.average_storage_percent()}% — {d.days_of_water_remaining()} days remaining")

    if green:
        print("\n  🟢 GREEN — Currently safe:")
        for d in sorted(green, key=lambda x: x.average_storage_percent()):
            print(f"     {d.name:20} {d.average_storage_percent()}%")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    MASTER_CSV = r"D:\maharashtra-jal-sankat-alert\data\raw\maharashtra_all_districts.csv"

    # All Maharashtra districts chart
    print("Generating all districts chart...")
    all_districts = load_all_districts(MASTER_CSV)
    plot_all_districts(all_districts)

    # Text summary
    print_district_summary(all_districts)