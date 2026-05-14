from reservoir import Reservoir


class District:
    """
    Represents a district in Maharashtra.
    Contains multiple reservoirs and tracks overall water situation.

    Real data source: Nashik District Government + Lokmat Times + CWC
    """

    def __init__(self, name, population, avg_annual_rainfall_mm,
                 daily_water_demand_mcft, drought_prone_talukas=None):
        """
        name                    : District name (e.g. 'Nashik')
        population              : Total population of district
        avg_annual_rainfall_mm  : Average annual rainfall in mm
        daily_water_demand_mcft : Daily water demand in million cubic feet
        drought_prone_talukas   : List of talukas that face drought frequently
        """
        self.name                    = name
        self.population              = population
        self.avg_annual_rainfall_mm  = avg_annual_rainfall_mm
        self.daily_water_demand_mcft = daily_water_demand_mcft
        self.drought_prone_talukas   = drought_prone_talukas or []
        self.reservoirs              = []   # list of Reservoir objects

    # ── Reservoir Management ─────────────────────────────────────────────────

    def add_reservoir(self, reservoir):
        """Add a Reservoir object to this district."""
        self.reservoirs.append(reservoir)

    def total_reservoirs(self):
        """Returns total number of reservoirs in district."""
        return len(self.reservoirs)

    # ── Water Level Analysis ─────────────────────────────────────────────────

    def total_capacity_mcft(self):
        """Returns total combined capacity of all reservoirs in MCft."""
        return sum(r.total_capacity for r in self.reservoirs)

    def average_storage_percent(self):
        """Returns average water level across all reservoirs as percentage."""
        if not self.reservoirs:
            return 0
        return round(sum(r.current_level for r in self.reservoirs) / len(self.reservoirs), 2)

    def critical_reservoirs(self):
        """Returns list of reservoirs that are in critical state (below 25%)."""
        return [r for r in self.reservoirs if r.is_critical()]

    def highest_risk_reservoir(self):
        """Returns the reservoir with the lowest water level."""
        if not self.reservoirs:
            return None
        return min(self.reservoirs, key=lambda r: r.current_level)

    def safest_reservoir(self):
        """Returns the reservoir with the highest water level."""
        if not self.reservoirs:
            return None
        return max(self.reservoirs, key=lambda r: r.current_level)

    # ── District Alert Level ─────────────────────────────────────────────────

    def district_alert_level(self):
        """
        Returns district-wide alert based on average storage.
        RED   : average below 25%
        AMBER : average between 25% and 50%
        GREEN : average above 50%
        """
        avg = self.average_storage_percent()
        if avg < 25:
            return "RED"
        elif avg < 50:
            return "AMBER"
        else:
            return "GREEN"

    # ── Water Supply Analysis ────────────────────────────────────────────────

    def days_of_water_remaining(self):
        """
        Estimates how many days of water supply remain across all reservoirs
        based on daily demand.
        Returns -1 if demand is 0.
        """
        if self.daily_water_demand_mcft == 0:
            return -1
        # total current water = sum of (capacity * level%) for all reservoirs
        total_current_water = sum(
            (r.total_capacity * r.current_level / 100) for r in self.reservoirs
        )
        return round(total_current_water / self.daily_water_demand_mcft)

    def rainfall_deficit_percent(self, actual_rainfall_mm):
        """
        Calculates how much below average the rainfall is this year.
        Positive = deficit. Negative = surplus.
        """
        deficit = self.avg_annual_rainfall_mm - actual_rainfall_mm
        return round((deficit / self.avg_annual_rainfall_mm) * 100, 2)

    def tanker_dependent_risk(self, actual_rainfall_mm):
        """
        Returns risk level of villages becoming tanker-dependent.
        Based on rainfall deficit + average storage.
        HIGH   : deficit > 25% AND storage < 40%
        MEDIUM : deficit > 15% OR storage < 40%
        LOW    : otherwise
        """
        deficit_pct = self.rainfall_deficit_percent(actual_rainfall_mm)
        avg_storage = self.average_storage_percent()

        if deficit_pct > 25 and avg_storage < 40:
            return "HIGH"
        elif deficit_pct > 15 or avg_storage < 40:
            return "MEDIUM"
        else:
            return "LOW"

    # ── Full District Report ─────────────────────────────────────────────────

    def generate_report(self, actual_rainfall_mm):
        """Prints a complete district water situation report."""
        print("=" * 60)
        print(f"  JAL SANKAT ALERT — {self.name.upper()} DISTRICT REPORT")
        print("=" * 60)
        print(f"  Population          : {self.population:,}")
        print(f"  Total Reservoirs    : {self.total_reservoirs()}")
        print(f"  Total Capacity      : {self.total_capacity_mcft():,.2f} MCft")
        print(f"  Average Storage     : {self.average_storage_percent()}%")
        print(f"  District Alert      : {self.district_alert_level()}")
        print(f"  Days of Water Left  : {self.days_of_water_remaining()} days")
        print(f"  Rainfall This Year  : {actual_rainfall_mm} mm")
        print(f"  Rainfall Deficit    : {self.rainfall_deficit_percent(actual_rainfall_mm)}%")
        print(f"  Tanker Risk         : {self.tanker_dependent_risk(actual_rainfall_mm)}")
        print()

        print("  RESERVOIR STATUS:")
        print("  " + "-" * 56)
        for r in sorted(self.reservoirs, key=lambda x: x.current_level):
            print(f"  {r}")
        print()

        critical = self.critical_reservoirs()
        if critical:
            print(f"  ⚠️  CRITICAL RESERVOIRS ({len(critical)}):")
            for r in critical:
                print(f"     → {r.dam_name} at {r.current_level}% — {r.days_to_critical()} days to critical")
        else:
            print("  ✅ No reservoirs in critical state")

        print()
        print(f"  Drought Prone Talukas: {', '.join(self.drought_prone_talukas)}")
        print("=" * 60)

    def __str__(self):
        return (
            f"{self.name} District | {self.total_reservoirs()} reservoirs | "
            f"Avg: {self.average_storage_percent()}% | {self.district_alert_level()}"
        )


# ── Real Nashik Data ─────────────────────────────────────────────────────────
# Sources:
# Population   : Census 2011 projected 2025
# Rainfall     : Nashik avg 700mm/year (district avg across talukas)
# Demand       : ~150 MCft/day estimated from population + agriculture
# Dam data     : Lokmat Times June 2025 + CWC records
# Drought data : Nashik Free Press Journal April 2025

if __name__ == "__main__":

    # Create Nashik district
    nashik = District(
        name                   = "Nashik",
        population             = 6_107_187,
        avg_annual_rainfall_mm = 700,
        daily_water_demand_mcft= 150,
        drought_prone_talukas  = ["Yeola", "Nandgaon", "Malegaon", "Sinnar", "Chandwad"]
    )

    # Add real Nashik reservoirs with actual data
    # Gangapur complex — primary drinking water source for Nashik city
    nashik.add_reservoir(Reservoir("Gangapur Dam",        "Nashik", 5575.0,  62.0, 0.35))
    nashik.add_reservoir(Reservoir("Kashyapi Dam",        "Nashik", 1836.0,  51.0, 0.30))
    nashik.add_reservoir(Reservoir("Gautami-Godavari Dam","Nashik", 1861.0,  33.0, 0.40))
    nashik.add_reservoir(Reservoir("Alandi Dam",          "Nashik",  812.0,  40.0, 0.25))

    # Other major Nashik dams
    nashik.add_reservoir(Reservoir("Darna Dam",           "Nashik", 5475.0,  58.0, 0.30))
    nashik.add_reservoir(Reservoir("Karanjvan Dam",       "Nashik", 5198.0,  28.0, 0.45))
    nashik.add_reservoir(Reservoir("Waghad Dam",          "Nashik", 2286.0,  27.0, 0.45))
    nashik.add_reservoir(Reservoir("Ozarkhed Dam",        "Nashik", 2098.0,  30.0, 0.40))
    nashik.add_reservoir(Reservoir("Palkhed Dam",         "Nashik",  648.0,  74.0, 0.20))
    nashik.add_reservoir(Reservoir("Punegaon Dam",        "Nashik",  601.0,  25.0, 0.50))
    nashik.add_reservoir(Reservoir("Tisgaon Dam",         "Nashik",  424.0,  10.0, 0.55))
    nashik.add_reservoir(Reservoir("Girna Dam",           "Nashik", 1516.0,  45.0, 0.35))

    # 2025 actual rainfall was significantly lower than average
    # Source: Nashik received 772.2mm vs 1035mm previous year
    actual_rainfall_2025 = 772

    # Generate full report
    nashik.generate_report(actual_rainfall_2025)

    # Quick summary
    print("\nQUICK SUMMARY:")
    print(nashik)
    print(f"Highest risk dam : {nashik.highest_risk_reservoir()}")
    print(f"Safest dam       : {nashik.safest_reservoir()}")