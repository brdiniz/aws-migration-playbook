#!/usr/bin/env python3
"""Compare the cost of staying on the current platform with moving to AWS.

Reads a JSON file (see examples/acme-saas.json) and prints:
  - monthly totals and the monthly delta
  - one-time costs, including the months both environments run in parallel
  - the break-even month
  - cumulative net savings at checkpoints, for three scenarios

Standard library only. All numbers are whatever you put in the input file.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

# Scenario multipliers applied to (target monthly costs, one-time costs).
SCENARIOS = {
    "optimistic": (0.8, 1.0),
    "expected": (1.0, 1.0),
    "pessimistic": (1.2, 1.5),
}


@dataclass
class Scenario:
    name: str
    current_monthly: float
    target_monthly: float  # includes ownership cost
    one_time: float  # includes double-running cost

    @property
    def monthly_delta(self) -> float:
        """Positive means AWS is cheaper per month."""
        return self.current_monthly - self.target_monthly

    @property
    def break_even_month(self) -> Optional[int]:
        if self.monthly_delta <= 0:
            return None
        return math.ceil(self.one_time / self.monthly_delta)

    def net_at(self, month: int) -> float:
        """Cumulative net savings after `month` months (negative = still paying back)."""
        return self.monthly_delta * month - self.one_time


def load(path: str) -> Dict:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    for key in ("current_monthly", "target_monthly", "one_time"):
        if not isinstance(data.get(key), dict) or not data[key]:
            raise ValueError(f"'{key}' must be a non-empty object of name -> amount")
    return data


def build_scenarios(data: Dict) -> List[Scenario]:
    current = sum(data["current_monthly"].values())
    target_base = sum(data["target_monthly"].values())
    ownership = float(data.get("ownership_monthly", 0))
    one_time_base = sum(data["one_time"].values())
    double_run = current * float(data.get("double_run_months", 0))

    scenarios = []
    for name, (target_mult, one_time_mult) in SCENARIOS.items():
        scenarios.append(
            Scenario(
                name=name,
                current_monthly=current,
                target_monthly=target_base * target_mult + ownership,
                one_time=(one_time_base * one_time_mult) + double_run,
            )
        )
    return scenarios


def _money(value: float) -> str:
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.0f}"


def render(data: Dict, scenarios: List[Scenario]) -> str:
    horizon = int(data.get("horizon_months", 36))
    checkpoints = sorted({m for m in (6, 12, 24, 36, horizon) if m <= horizon})
    lines = [f"Migration cost comparison: {data.get('company', 'unnamed')}", ""]

    lines.append("Monthly costs")
    lines.append(f"  Current platform: {_money(scenarios[0].current_monthly)}")
    for s in scenarios:
        lines.append(
            f"  AWS ({s.name}): {_money(s.target_monthly)}  "
            f"(monthly delta {_money(s.monthly_delta)})"
        )
    lines.append("")

    header = f"{'Scenario':<13}{'One-time':>12}{'Break-even':>13}" + "".join(
        f"{'Net @' + str(m) + 'm':>14}" for m in checkpoints
    )
    lines.append(header)
    lines.append("-" * len(header))
    for s in scenarios:
        be = f"month {s.break_even_month}" if s.break_even_month else "never"
        row = f"{s.name:<13}{_money(s.one_time):>12}{be:>13}" + "".join(
            f"{_money(s.net_at(m)):>14}" for m in checkpoints
        )
        lines.append(row)
    lines.append("")
    lines.append(
        "Net = cumulative savings minus one-time costs. Negative means the migration has not paid back yet."
    )
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", help="Path to the JSON input file")
    args = parser.parse_args(argv)
    try:
        data = load(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(render(data, build_scenarios(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
