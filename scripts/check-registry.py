#!/usr/bin/env python3
"""Validate the Codex role registry: schema-conformance + referential integrity.

Enforces what JSON Schema alone cannot express:
  1. data/roles.json conforms to schema/role-registry.schema.json (JSON Schema 2020-12).
  2. every role's `accessibleFallback` names a role that actually exists here (the
     accessibility floor must resolve to a real, operable role — never a dangling name).
  3. every role's `gatedBy` (mode-gating, when present) names a role that exists here.

Exit 0 = clean; non-zero = a defect. Intended as the repo's CI gate (arms on a remote,
like CommonTongue's `buf` breaking gate). Run: python3 scripts/check-registry.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "role-registry.schema.json"
DATA = ROOT / "data" / "roles.json"


def main() -> int:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print("ERROR: pip install jsonschema (>=4) is required", file=sys.stderr)
        return 2

    schema = json.loads(SCHEMA.read_text())
    data = json.loads(DATA.read_text())

    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))
    if errors:
        print(f"SCHEMA INVALID — {len(errors)} error(s):")
        for e in errors:
            print(f"  • {list(e.path)}: {e.message}")
        return 1

    roles = data["roles"]
    names = {r["role"] for r in roles}
    fallback_dangling = [
        (r["role"], r["accessibleFallback"])
        for r in roles
        if r["accessibleFallback"] not in names
    ]
    gate_dangling = [
        (r["role"], r["gatedBy"])
        for r in roles
        if r.get("gatedBy") and r["gatedBy"] not in names
    ]
    if fallback_dangling or gate_dangling:
        for role, target in fallback_dangling:
            print(f"  • role '{role}' accessibleFallback '{target}' is not a registered role")
        for role, target in gate_dangling:
            print(f"  • role '{role}' gatedBy '{target}' is not a registered role")
        print(f"REFERENTIAL INTEGRITY — {len(fallback_dangling) + len(gate_dangling)} dangling reference(s).")
        return 1

    print(f"OK — {len(roles)} roles: schema-valid (draft-2020-12) and every "
          f"accessibleFallback/gatedBy resolves to a real role.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
