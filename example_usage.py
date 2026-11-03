"""
Example Usage: Pulmonary Dynamic Hyperinflation & Inspiratory Capacity (IC) Tracking.
Demonstrates zero-dependency calculation of exertional IC drop, EELV shift, and mechanical ventilatory mechanics scoring.
"""

from client import PulmonaryDynamicHyperinflationClient


def main():
    client = PulmonaryDynamicHyperinflationClient()
    print("=== Pulmonary Dynamic Hyperinflation (DH) Demo ===")

    # Test Case 1: Healthy athlete during vigorous treadmill ramp
    res1 = client.evaluate_dynamic_hyperinflation(
        resting_inspiratory_capacity_l=3.4,
        exertional_inspiratory_capacity_l=3.45,
        total_lung_capacity_l=6.5,
        resting_tidal_volume_l=0.68,
        exertional_minute_ventilation_l_min=55.0
    )
    print("\nTest Case 1: Stable Exertional IC (Normal Ventilatory Mechanics)")
    print(f"  Resting IC: {res1['resting_inspiratory_capacity_l']} L | Exertional IC: {res1['exertional_inspiratory_capacity_l']} L")
    print(f"  Delta IC: {res1['delta_ic_l']} L (EELV shift: {res1['eelv_shift_l']} L)")
    print(f"  Estimated IRV: {res1['estimated_exertional_irv_l']} L | IC % TLC: {res1['exertional_ic_tlc_pct']}%")
    print(f"  Ventilatory Score: {res1['ventilatory_mechanics_score']} / 100")
    print(f"  Classification: {res1['classification']}")
    print(f"  Physiological Interpretation: {res1['physiological_interpretation']}")
    print(f"  Actionable Guidance: {res1['actionable_guidance']}")

    # Test Case 2: Significant dynamic hyperinflation / air trapping
    res2 = client.evaluate_dynamic_hyperinflation(
        resting_inspiratory_capacity_l=2.9,
        exertional_inspiratory_capacity_l=2.45,
        total_lung_capacity_l=5.8,
        resting_tidal_volume_l=0.60,
        exertional_minute_ventilation_l_min=38.0
    )
    print("\nTest Case 2: Significant Dynamic Hyperinflation Pattern")
    print(f"  Delta IC: {res2['delta_ic_l']} L (EELV shift: +{res2['eelv_shift_l']} L)")
    print(f"  Estimated IRV: {res2['estimated_exertional_irv_l']} L")
    print(f"  Ventilatory Score: {res2['ventilatory_mechanics_score']} / 100")
    print(f"  Classification: {res2['classification']}")
    print(f"  Actionable Guidance: {res2['actionable_guidance']}")


if __name__ == "__main__":
    main()
