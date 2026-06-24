#!/usr/bin/env python3
"""Generate a simple, illustrative APS pension statement from the sample data.

This is a teaching demo. The projection is intentionally simple and uses
fictional data in demos/sample-data/members.json. It is NOT an official quote.

Usage:
    python generate_statement.py --member M-1003
    python generate_statement.py --member M-1003 --format json
    python generate_statement.py --data /path/to/members.json --member M-1002
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Simple, clearly-stated projection assumptions (teaching only).
ANNUAL_GROWTH = 0.04          # assumed growth on the accrued value
ANNUAL_PAYOUT_RATE = 0.05     # assumed yearly pension as a share of the pot at retirement


def default_data_path() -> Path:
    """Locate demos/sample-data/members.json relative to this script."""
    # scripts -> pension-statement -> skills -> .github -> demos
    demos_root = Path(__file__).resolve().parents[4]
    return demos_root / "sample-data" / "members.json"


def load_members(data_path: Path) -> dict:
    if not data_path.exists():
        raise FileNotFoundError(f"Sample data not found at: {data_path}")
    with data_path.open(encoding="utf-8") as fh:
        return json.load(fh)


def find_member(data: dict, member_id: str) -> dict | None:
    target = member_id.strip().lower()
    for m in data.get("members", []):
        if m["id"].lower() == target:
            return m
    return None


def project(member: dict) -> dict:
    """Return a simple retirement projection for one member."""
    years = max(0, member["targetRetirementAge"] - member["age"])
    annual_contrib = member["monthlyContribution"] * 12

    # Grow the existing pot, plus contributions added each year and grown.
    value = member["accruedValue"]
    for _ in range(years):
        value = value * (1 + ANNUAL_GROWTH) + annual_contrib

    projected_value = round(value)
    projected_monthly = round(projected_value * ANNUAL_PAYOUT_RATE / 12)

    return {
        "yearsToRetirement": years,
        "projectedValue": projected_value,
        "projectedMonthlyPension": projected_monthly,
    }


def money(n: int | float) -> str:
    return f"${int(round(n)):,}"


def render_text(member: dict, proj: dict, as_of: str) -> str:
    s = member["sources"]
    lines = [
        f"APS PENSION STATEMENT  ·  As of {as_of}",
        f"Member: {member['name']} ({member['id']})",
        "",
        f"Your pension savings        {money(member['monthlyContribution'])}/month",
        "",
        f"Your accrued pension        {money(member['accruedValue'])}",
        f"  Public      {money(s['public'])}",
        f"  Workplace   {money(s['workplace'])}",
        f"  Personal    {money(s['personal'])}",
        "",
        f"Your forecast at retirement {money(proj['projectedMonthlyPension'])}/month before tax",
        f"  Retiring at age {member['targetRetirementAge']} "
        f"(in {proj['yearsToRetirement']} years)",
        f"  Estimated value at retirement: {money(proj['projectedValue'])}",
        "",
        "Note: Illustrative figures based on fictional sample data and a simplified",
        "projection. Not an official APS quote. For decisions about your own pension,",
        "contact APS directly.",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate an APS pension statement.")
    parser.add_argument("--member", required=True, help="Member id, e.g. M-1003")
    parser.add_argument("--data", type=Path, default=None, help="Path to members.json")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    data_path = args.data or default_data_path()
    try:
        data = load_members(data_path)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    member = find_member(data, args.member)
    if member is None:
        available = ", ".join(m["id"] for m in data.get("members", []))
        print(f"Error: member '{args.member}' not found. Available: {available}",
              file=sys.stderr)
        return 2

    proj = project(member)
    as_of = data.get("asOf", "today")

    if args.format == "json":
        print(json.dumps({**member, "projection": proj, "asOf": as_of}, indent=2))
    else:
        print(render_text(member, proj, as_of))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
