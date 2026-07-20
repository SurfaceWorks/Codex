# Codex — Decision Log

The record of what has been decided, rejected, and left open for the `Codex` repo (the family's
role-vocabulary registry). Per the family decision-doctrine: status + why + provenance; nothing
deleted to tidy.

**Provenance:** `[V]` verified · `[D]` documented · `[A]` assumed. **Statuses:** proposed · accepted
· superseded. Only the owner promotes to accepted.

---

### D-001 — Registry form = JSON-Schema-validated data registry
- **Status:** accepted
- **Date:** 2026-07-19
- **What:** The role vocabulary is published as **data** (`data/roles.json`) validated by a **JSON
  Schema 2020-12** (`schema/role-registry.schema.json`). The prose registry
  (`docs/reference/2026-07-19-role-registry.md`) stays as **human narration** and points at the data
  as the authoritative machine artifact. The `role` identifier is an **open string** (standard
  `lowercase_snake`, or a vendor tail `x.<vendor>.<name>`) — never a closed enum — so the vocabulary
  stays open, grows by PR, and an unrecognised role still renders (its required `unmappedFallback`, or
  the generic `unmapped` role). Each entry MUST carry `surfaceType` (A/B/AB), `nature` (W/R/A — the
  honesty axis: settable vs. observed vs. fired), and `unmappedFallback` (the interop/accessibility
  floor) — all **schema-enforced**. Optional `valueShape` (scalar/compound/array) and `gatedBy`
  (mode-gating, e.g. colour roles gated by `color_mode`) capture the richer structure.
- **Why — evaluated against all four lenses (owner-directed, 2026-07-19). Identical analysis to
  Palette D-001** (the two registries share one form decision):
  - **North Stars** (Lucidity's, in order — Accessibility · Ease-of-use · Speed · Choice): leans
    JSON. Required fields (`unmappedFallback`, `nature`) as JSON-Schema `required` are **hard
    authoring-time failures** — the interop/honesty floor is structural, not diligence (proto3 has no
    true required). Grow-by-PR = add a row; no codegen cycle.
  - **BP (blueprints / SHAPES layer):** **not applicable** — a role *registry* consumed by a
    *renderer* is not the `simple-hardware-controller-service` shape (SurfaceWorks is
    control-flow-inverted vs. the blueprint). Stated, not skipped.
  - **Best Practices:** a validated **data registry** is the idiomatic form for an open,
    recommended-not-required, grow-by-PR vocabulary where unknown values are expected — not a compiled
    proto (whose value is a frozen wire contract with generated types).
  - **Correctness / single-source-of-truth:** role **meaning**, the **value model**
    (compound/array), and **mode-gating** are owned by the **CommonTongue** contract and only
    **referenced** here (`valueShape`/`gatedBy` are hints that name contract concepts, not
    redefinitions). The CommonTongue link is a documented **convention-reference**, not a proto
    `import` — an accepted, marked tradeoff. Referential integrity within the registry (every
    `unmappedFallback`/`gatedBy` resolves to a real role) is verified `[V]`.
- **Rejected alternatives:** same as Palette D-001 — closed proto enum (violates open/growable;
  `buf breaking` enum-blind); proto importing CommonTongue (**verification-blocked** — buf v2 deps are
  BSR-only, no shared workspace across orgs, CommonTongue not on a BSR `[V]`); publish CommonTongue to
  a BSR + proto (only idiomatic proto path, but a standing dependency for a small shared surface).
- **Provenance:** `[V]` — schema valid draft-2020-12; 196 roles validate; negative controls confirm
  rejection of missing `unmappedFallback`/`nature`, bad `nature`/`surfaceType`/`group`, and stray
  properties, and acceptance of a vendor-tail `role`; referential integrity holds. Owner ratified the
  form + JSON-Schema 2020-12 + this decision log, 2026-07-19.

---

## Open items — do NOT build on these

### O-101 — Vocabulary is a prototype, not frozen
- **State:** open. `data/roles.json` `status: prototype` — the role set moves as Lucidity and other
  renderers build against it. Coverage target: standard 90%; the long tail is a product's own
  extension (`unmapped` or a vendor role).
- **Closes when:** the owner promotes the vocabulary to `stable` (a one-way cut the owner triggers,
  not the agent).
