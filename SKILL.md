---
name: genpark-personal-agent-pulmonary-dynamic-hyperinflation-ic-skill
version: 1.0.0
description: Zero-dependency sovereign personal agent skill for calculating exertional Inspiratory Capacity drop (Delta IC), End-Expiratory Lung Volume (EELV) air trapping, and ventilatory mechanics reserve.
author: AlphaPark Inc.
license: Apache-2.0
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
metadata:
  openclaw_compatible: true
  hermes_compatible: true
  zero_dependency: true
---

# Pulmonary Dynamic Hyperinflation (IC Tracking) Skill

A sovereign personal agent capability for monitoring exercise-induced expiratory flow limitation, Inspiratory Capacity (IC) decrement, End-Expiratory Lung Volume ($EELV$) shift, and intrinsic PEEP during physical training or breathwork.

## Core Capabilities
- **Inspiratory Capacity (IC) Dynamics**: Quantifies exertional lung volume changes ($\Delta IC = IC_{exertion} - IC_{rest}$ in Liters).
- **Dynamic Air Trapping Detection**: Identifies acute rises in $EELV$ ($\Delta EELV = -\Delta IC \ge +0.25\text{ L}$), indicating gas trapping behind narrowed bronchioles.
- **Inspiratory Reserve Volume (IRV) Preservation**: Tracks remaining headroom ($IRV$) between peak tidal inhalation and Total Lung Capacity ($TLC$).
- **Expiratory Flow Optimization**: Prescribes pursed-lip exhalation techniques (1:2 to 1:3 inspiratory-to-expiratory ratio) to mitigate exertional breathlessness.

## Fast Invocation
```python
from client import PulmonaryDynamicHyperinflationClient

client = PulmonaryDynamicHyperinflationClient()
res = client.evaluate_dynamic_hyperinflation(
    resting_inspiratory_capacity_l=3.4,
    exertional_inspiratory_capacity_l=3.45,
    total_lung_capacity_l=6.5
)
print("Delta IC:", res["delta_ic_l"], "L")
print("Ventilatory Score:", res["ventilatory_mechanics_score"], "/ 100")
```
