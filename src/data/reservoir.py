class Reservoir:
    """
    Represents a single reservoir/dam in Maharashtra.
    Tracks water levels and predicts shortage risk.
    """

    def __init__(self, dam_name, district, total_capacity, current_level, daily_depletion_rate=0.3):
        """
        dam_name            : Name of the dam (e.g. 'Koyna Dam')
        district            : District it belongs to (e.g. 'Satara')
        total_capacity      : Total capacity in TMC (Thousand Million Cubic feet)
        current_level       : Current water level as percentage (0 to 100)
        daily_depletion_rate: How much % is lost per day on average (default 0.3)
        """
        self.dam_name             = dam_name
        self.district             = district
        self.total_capacity       = total_capacity
        self.current_level        = current_level
        self.daily_depletion_rate = daily_depletion_rate

    def storage_percent(self):
        """Returns current water level as a percentage."""
        return self.current_level

    def is_critical(self):
        """Returns True if water level is below 25%."""
        return self.current_level < 25

    def alert_level(self):
        """
        Returns alert level based on current water level.
        RED   : below 25%  — immediate risk
        AMBER : 25% to 50% — monitor closely
        GREEN : above 50%  — stable
        """
        if self.current_level < 25:
            return "RED"
        elif self.current_level < 50:
            return "AMBER"
        else:
            return "GREEN"

    def days_to_empty(self):
        """
        Estimates days until reservoir hits 0%.
        Returns 0 if already empty.
        Returns -1 if depletion rate is 0 (no depletion).
        """
        if self.current_level <= 0:
            return 0
        if self.daily_depletion_rate == 0:
            return -1  # no depletion happening
        return round(self.current_level / self.daily_depletion_rate)

    def days_to_critical(self):
        """
        Estimates days until reservoir hits critical level (25%).
        Returns 0 if already at or below critical.
        """
        if self.current_level <= 25:
            return 0
        if self.daily_depletion_rate == 0:
            return -1  # no depletion happening
        remaining_before_critical = self.current_level - 25
        return round(remaining_before_critical / self.daily_depletion_rate)

    def __str__(self):
        """Human readable summary of the reservoir."""
        return (
            f"{self.dam_name} | {self.district} | "
            f"{self.current_level}% | {self.alert_level()} | "
            f"Critical in {self.days_to_critical()} days"
        )


# ── Test ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    koyna  = Reservoir("Koyna Dam",   "Satara", 105.25, 45.2, 0.3)
    latur  = Reservoir("Manjara Dam", "Latur",    9.47, 18.3, 0.5)
    nashik = Reservoir("Gangapur Dam","Nashik",   5.57, 72.1, 0.2)

    dams = [koyna, latur, nashik]

    print("=" * 55)
    print("  Maharashtra Jal Sankat Alert — Reservoir Report")
    print("=" * 55)

    for dam in dams:
        print(dam)

    print("\n--- Critical Dams ---")
    for dam in dams:
        if dam.is_critical():
            print(f"  WARNING: {dam.dam_name} is CRITICAL at {dam.current_level}%")

    print("\n--- Days to Critical ---")
    for dam in dams:
        days = dam.days_to_critical()
        if days == 0:
            print(f"  {dam.dam_name}: Already critical!")
        else:
            print(f"  {dam.dam_name}: {days} days to critical level")