"""
MCP Server for Pulmonary Dynamic Hyperinflation & Inspiratory Capacity (IC) Skill.
Exposes JSON-RPC Model Context Protocol tools for evaluating exertional IC drops, EELV shifts, and ventilatory scores.
"""

import sys
import json
from typing import Dict, Any
from client import PulmonaryDynamicHyperinflationClient


def get_tools_manifest() -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "evaluate_dynamic_hyperinflation",
                "description": "Calculates exertional Inspiratory Capacity drop (Delta IC in L), End-Expiratory Lung Volume (EELV) shift, IRV reserve, and ventilatory mechanics score.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resting_inspiratory_capacity_l": {
                            "type": "number",
                            "description": "Resting baseline Inspiratory Capacity in liters (e.g. 3.2 L)."
                        },
                        "exertional_inspiratory_capacity_l": {
                            "type": "number",
                            "description": "Inspiratory Capacity measured during peak or submaximal exertion in liters (e.g. 2.8 L)."
                        },
                        "total_lung_capacity_l": {
                            "type": "number",
                            "description": "Total Lung Capacity (TLC) in liters (e.g. 6.2 L)."
                        },
                        "resting_tidal_volume_l": {
                            "type": "number",
                            "description": "Resting tidal volume in liters (default: 0.65 L).",
                            "default": 0.65
                        },
                        "exertional_minute_ventilation_l_min": {
                            "type": "number",
                            "description": "Minute ventilation during exercise challenge in L/min (default: 45.0 L/min).",
                            "default": 45.0
                        }
                    },
                    "required": ["resting_inspiratory_capacity_l", "exertional_inspiratory_capacity_l", "total_lung_capacity_l"]
                }
            }
        ]
    }


def handle_request(client: PulmonaryDynamicHyperinflationClient, req: Dict[str, Any]) -> Dict[str, Any]:
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": get_tools_manifest()
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})

        if name == "evaluate_dynamic_hyperinflation":
            res = client.evaluate_dynamic_hyperinflation(
                resting_inspiratory_capacity_l=float(args.get("resting_inspiratory_capacity_l", 3.0)),
                exertional_inspiratory_capacity_l=float(args.get("exertional_inspiratory_capacity_l", 2.9)),
                total_lung_capacity_l=float(args.get("total_lung_capacity_l", 6.0)),
                resting_tidal_volume_l=float(args.get("resting_tidal_volume_l", 0.65)),
                exertional_minute_ventilation_l_min=float(args.get("exertional_minute_ventilation_l_min", 45.0))
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res, indent=2)
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {name}"
                }
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32600,
                "message": f"Invalid Request: Unsupported method {method}"
            }
        }


def main():
    client = PulmonaryDynamicHyperinflationClient()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(client, req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error or exception: {str(e)}"
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
