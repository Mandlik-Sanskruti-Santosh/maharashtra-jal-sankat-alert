class Reservoir:
    def __init__(self, dam_name, district, total_capacity, current_level):
        self.dam_name = dam_name
        self.district = district
        self.total_capacity = total_capacity
        self.current_level = current_level

    def storage_percent(self):   # ← 4 spaces indent = inside class
        return self.current_level

# Test
koyna = Reservoir("Koyna Dam", "Satara", 105.25, 45.2)
print(koyna.dam_name)
print(koyna.storage_percent())