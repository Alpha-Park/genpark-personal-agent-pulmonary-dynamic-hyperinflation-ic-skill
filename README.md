# Pulmonary Dynamic Hyperinflation (IC Tracking) Skill

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/zero--dependencies-standard--lib-brightgreen.svg)](requirements.txt)
[![MCP Protocol Ready](https://img.shields.io/badge/mcp-protocol--ready-orange.svg)](mcp_server.py)
[![OpenClaw Certified](https://img.shields.io/badge/openclaw-certified-purple.svg)](SKILL.md)

Zero-dependency sovereign personal agent skill for non-invasive evaluation of exertional Inspiratory Capacity drop (Delta IC), End-Expiratory Lung Volume (EELV) air trapping, and ventilatory mechanics reserve.

```mermaid
flowchart TD
    RestingIC["Resting Inspiratory Capacity (IC_rest) Baseline"] --> ExertionRamp["Physical Exertion / Hyperventilation Challenge"]
    ExertionRamp --> ExertionalIC["Serial Exertional Inspiratory Capacity Maneuvers (IC_ex)"]
    ExertionalIC --> DeltaIC_Calc["Delta IC (L) & End-Expiratory Lung Volume Shift (EELV)"]
    DeltaIC_Calc --> IRV_Encroachment["Inspiratory Reserve Volume (IRV) Compression Analysis"]
    IRV_Encroachment --> DynamicScore["Exertional Ventilatory Mechanics & Dyspnea Risk Score"]
    DynamicScore --> Agent["OpenClaw / Hermes Personal Agent Paced Breathing Coaching"]
```

## Features
- **Deterministic Math**: Pure Python standard library implementation with zero external dependencies.
- **Cardiopulmonary Exercise Testing (CPET) Standards**: Implements validated equations for serial IC tracking, EELV shifts, and IRV ceiling limits.
- **Dynamic Air Trapping & Dyspnea Prevention**: Early detection of mechanical diaphragm disadvantage during intense workouts or cardio intervals.
- **Model Context Protocol (MCP)**: Native JSON-RPC tool integration for LLMs and autonomous agents.

## Quickstart

```python
from client import PulmonaryDynamicHyperinflationClient

client = PulmonaryDynamicHyperinflationClient()
result = client.evaluate_dynamic_hyperinflation(
    resting_inspiratory_capacity_l=3.4,
    exertional_inspiratory_capacity_l=3.45,
    total_lung_capacity_l=6.5
)
print("Delta IC:", result["delta_ic_l"], "L")
print("Ventilatory Score:", result["ventilatory_mechanics_score"])
print("Classification:", result["classification"])
```

## License
Apache-2.0
