"""
Pulmonary Dynamic Hyperinflation & Inspiratory Capacity (IC) Tracking Engine.
Provides deterministic, zero-dependency modeling of exertional Inspiratory Capacity drop,
End-Expiratory Lung Volume (EELV) shift, Inspiratory Reserve Volume (IRV) encroachment, and mechanical ventilatory limitation.
"""

from typing import Dict, Any, List, Optional


class PulmonaryDynamicHyperinflationClient:
    """
    Deterministic client for calculating Dynamic Hyperinflation (DH) during exertion or tachypnea.
    Assesses expiratory flow limitation, intrinsic positive end-expiratory pressure (auto-PEEP),
    diaphragmatic mechanical shortening, and exertional dyspnea thresholds.
    """

    def __init__(self):
        pass

    def evaluate_dynamic_hyperinflation(
        self,
        resting_inspiratory_capacity_l: float,
        exertional_inspiratory_capacity_l: float,
        total_lung_capacity_l: float,
        resting_tidal_volume_l: float = 0.65,
        exertional_minute_ventilation_l_min: float = 45.0
    ) -> Dict[str, Any]:
        """
        Calculates IC change: Delta_IC = exertional_IC - resting_IC.
        Normative values:
        - Healthy: Delta_IC >= 0.0 L (IC stable or increases slightly during exertion)
        - Mild Hyperinflation: -0.24 L <= Delta_IC < -0.10 L
        - Significant Dynamic Hyperinflation: Delta_IC <= -0.25 L
        - Critical IRV limit: IRV < 0.50 L
        """
        if resting_inspiratory_capacity_l <= 0 or exertional_inspiratory_capacity_l <= 0 or total_lung_capacity_l <= 0:
            return {"error": "Lung volumes must be strictly positive"}
        if resting_inspiratory_capacity_l > total_lung_capacity_l or exertional_inspiratory_capacity_l > total_lung_capacity_l:
            return {"error": "Inspiratory capacity cannot exceed total lung capacity"}

        # 1. Delta Inspiratory Capacity (L)
        delta_ic_l = round(exertional_inspiratory_capacity_l - resting_inspiratory_capacity_l, 2)

        # 2. End-Expiratory Lung Volume (EELV) shift (L) -> positive indicates air trapping
        eelv_shift_l = round(-delta_ic_l, 2)

        # 3. Exertional IC % of TLC
        exertional_ic_tlc_pct = round((exertional_inspiratory_capacity_l / total_lung_capacity_l) * 100.0, 1)

        # 4. Estimated Exertional Inspiratory Reserve Volume (IRV = IC_ex - 1.5 * VT_rest)
        est_exertional_vt_l = min(exertional_inspiratory_capacity_l * 0.7, resting_tidal_volume_l * 2.2)
        irv_l = round(max(0.1, exertional_inspiratory_capacity_l - est_exertional_vt_l), 2)

        # 5. Exertional Ventilatory Mechanics Score (0 - 100)
        score = 80.0
        if delta_ic_l >= 0.0:
            score += 15.0
        elif delta_ic_l >= -0.12:
            score += 5.0
        elif delta_ic_l <= -0.35:
            score -= 32.0  # Severe dynamic air trapping
        elif delta_ic_l <= -0.25:
            score -= 18.0

        if irv_l >= 0.70:
            score += 5.0
        elif irv_l < 0.40:
            score -= 20.0  # Approaching ceiling of TLC

        if exertional_ic_tlc_pct >= 40.0:
            score += 5.0
        elif exertional_ic_tlc_pct < 28.0:
            score -= 12.0

        vent_score = round(min(100.0, max(5.0, score)), 1)

        if vent_score >= 85.0 and delta_ic_l >= -0.08:
            tier = "OPTIMAL_VENTILATORY_EXPIRATORY_MECHANICS"
            interp = f"Preserved exertional inspiratory capacity (Delta IC {delta_ic_l} L, IRV {irv_l} L); no exercise-induced dynamic air trapping."
            guidance = "Excellent pulmonary biomechanical reserve. Diaphragm maintains optimal length-tension advantage across high ventilatory workloads."
        elif delta_ic_l <= -0.25 or irv_l < 0.45:
            tier = "SIGNIFICANT_DYNAMIC_HYPERINFLATION"
            interp = f"Marked exertional air trapping (Delta IC {delta_ic_l} L <= -0.25 L, EELV increase +{eelv_shift_l} L, critical IRV {irv_l} L); reflects expiratory flow limitation and auto-PEEP accumulation."
            guidance = "Dynamic hyperinflation detected. Practice pursed-lip exhalation (1:2 to 1:3 inspiratory-to-expiratory ratio) to prolong exhalation time and prevent air trapping."
        else:
            tier = "MILD_EXERTIONAL_AIR_TRAPPING"
            interp = f"Modest inspiratory capacity decrement (Delta IC {delta_ic_l} L, EELV shift +{eelv_shift_l} L); borderline expiratory reserve encroachment."
            guidance = "Maintain moderate endurance training with conscious pacing; monitor for respiratory muscle fatigue during interval cardio."

        return {
            "resting_inspiratory_capacity_l": resting_inspiratory_capacity_l,
            "exertional_inspiratory_capacity_l": exertional_inspiratory_capacity_l,
            "total_lung_capacity_l": total_lung_capacity_l,
            "delta_ic_l": delta_ic_l,
            "eelv_shift_l": eelv_shift_l,
            "exertional_ic_tlc_pct": exertional_ic_tlc_pct,
            "estimated_exertional_irv_l": irv_l,
            "exertional_minute_ventilation_l_min": exertional_minute_ventilation_l_min,
            "ventilatory_mechanics_score": vent_score,
            "classification": tier,
            "physiological_interpretation": interp,
            "actionable_guidance": guidance
        }
