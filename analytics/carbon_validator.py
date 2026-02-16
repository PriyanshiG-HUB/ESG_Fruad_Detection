# analytics/carbon_validator.py

import json
import math

def validate_carbon_claims(carbon_data, epa_emissions):
    """
    Validate reported CO2 emissions using fuel-based calculation
    and EPA emissions comparison.
    """

    # Emission factors (kg CO2 per unit fuel – simplified)
    EMISSION_FACTORS = {
        "natural_gas": 53.06,
        "diesel": 74.96,
        "coal": 95.52
    }

    reported = carbon_data["reported_co2"]

    # Step 1: Calculate CO2 from fuel usage
    calculated = 0
    for fuel, amount in carbon_data["fuel_usage"].items():
        if fuel in EMISSION_FACTORS:
            calculated += EMISSION_FACTORS[fuel] * amount

    # Step 2: Discrepancy percentage
    discrepancy_percent = abs(reported - calculated) / reported * 100

    # Step 3: Compare with EPA emissions
    epa_difference = abs(reported - epa_emissions) / reported * 100

    # Step 4: Z-score (assume 10% uncertainty)
    uncertainty = calculated * 0.10
    z_score = (reported - calculated) / uncertainty if uncertainty != 0 else 0

    # Step 5: Flag significant mismatch
    significant_mismatch = abs(z_score) > 1.96 or discrepancy_percent > 15

    return {
        "reported_co2": reported,
        "calculated_co2": round(calculated, 2),
        "epa_emissions": round(epa_emissions, 2),
        "fuel_discrepancy_percent": round(discrepancy_percent, 2),
        "epa_discrepancy_percent": round(epa_difference, 2),
        "z_score": round(z_score, 2),
        "carbon_fraud_flag": significant_mismatch
    }