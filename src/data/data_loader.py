import csv
from reservoir import Reservoir

def load_reservoirs_from_csv(filepath):
    reservoirs = []
    
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reservoir = Reservoir(
                dam_name =  row['dam_name'],            
                district = row['district'],
                total_capacity = float(row['total_capacity']),  # convert to float
                current_level = float(row['current_level']),   # convert to float
                daily_depletion_rate = float(row['daily_depletion_rate']),  # convert to float
            )
            reservoirs.append(reservoir)
    
    return reservoirs

if __name__ == "__main__":
    reservoirs = load_reservoirs_from_csv(r"D:\maharashtra-jal-sankat-alert\data\raw\nashik_dams.csv")
    
    print(f"Loaded {len(reservoirs)} reservoirs\n")
    for r in reservoirs:
        print(r)