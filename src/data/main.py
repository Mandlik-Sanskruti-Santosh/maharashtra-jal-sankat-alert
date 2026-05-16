from data_loader import load_reservoirs_from_csv
from district import District

# Step 1 — Create Nashik district
nashik = District(
    name = "Nashik",
    population = 6_107_187,
    avg_annual_rainfall_mm = 700,
    daily_water_demand_mcft = 150,
    drought_prone_talukas = ["Yeola", "Nandgaon", "Malegaon", "Sinnar", "Chandwad"]
)

# Step 2 — Load reservoirs from CSV
reservoirs = load_reservoirs_from_csv(r"D:\maharashtra-jal-sankat-alert\data\raw\nashik_dams.csv")

# Step 3 — Add all reservoirs to district
for reservoir in reservoirs:
    nashik.add_reservoir(reservoir)

# Step 4 — Generate full report
nashik.generate_report(772)