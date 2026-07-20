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

### D-002 — `nature` is a coarse role-capability axis; read-write vs write-only lives in the contract
- **Status:** accepted
- **Date:** 2026-07-19
- **What:** `nature` changed from `W / R / A` to **`settable` / `readonly` / `action`** — the coarse
  ROLE-level capability (does a client set it, observe it, or fire it). The registry **no longer**
  attempts to state read-write vs write-only. That read/write/confidence honesty is a per-**device**
  fact already owned by the **CommonTongue** descriptor: `PropertyPayload.Access`
  (READ_ONLY / READ_WRITE / WRITE_ONLY) plus the value `Confidence` axis
  (CONFIRMED / COMMANDED / UNKNOWN / STALE — "commanded ≠ confirmed" for a write-only device).
- **Why — the old `W` was an active correctness defect, confirmed against three lenses + doctrine:**
  - **Correctness / single-source-of-truth:** a bare `W` conflated *read-write* (settable **and**
    observable) with *write-only* (settable, **no readback ever**), and could express neither honestly.
    The same role is read-write on a device that reports back and **write-only** on one that does not
    (a real owned example: a write-only fixture — you send intensity/CCT and it never reports back).
    Read-back-ness is therefore a **device** fact, not a **role** fact; pinning it on the role made
    Codex lie about half of all devices. It also **duplicated** an axis the contract already owns
    (`Access` + `Confidence`) — restating, not referencing (SoT violation). Fix: stop restating;
    Codex holds only the coarse axis and references the contract for RW/WO/RO.
  - **Best Practices:** RW / WO / RO is the standard access-mode vocabulary (W3C WoT `readOnly`/
    `writeOnly`; OPC-UA AccessLevel; MODBUS; register RO/WO/RW conventions; the WoT
    property/action/event split = our settable/readonly/action). A bare `W` with no RW/WO distinction
    is the non-idiomatic outlier. The idiomatic home for RW/WO/RO is per-property on the descriptor —
    which is exactly where CommonTongue already put it (`PropertyPayload.Access`).
  - **North Stars (Accessibility #1):** a renderer must announce the truth about a control's state; a
    write-only control must render/announce *commanded, unconfirmed*, never a fabricated confirmed
    value (confidence-scoring §7 "never ship a guessed value dressed as a measured one"; ws-control §2
    write-only case). The coarse `settable` + the descriptor's `Access`/`Confidence` carry that truth;
    a bare `W` erased it.
  - **Doctrine already decided this:** ws-control-doctrine §2 names write-only as the "extreme case
    that proves the rule"; cold-start-acceptance names write-only devices explicitly; the contract's
    `Confidence.COMMANDED` comment already reads "no readback exists (a write-only device's normal
    state)." The contract was right; Codex's `nature` was the thing out of step.
- **Supersedes:** the `nature: W/R/A` portion of D-001. Rest of D-001 (JSON-Schema data-registry form)
  stands.
- **Provenance:** `[V]` — schema valid draft-2020-12; 196 roles revalidate (118 settable / 42 readonly
  / 36 action); negative controls confirm the old `W` is now **rejected**; referential integrity holds.

---

### D-003 — Critical-lens audit fixes (SoT, altitude, a11y wording, enforcement)
- **Status:** accepted
- **Date:** 2026-07-19
- **What:** A critical re-read of the schema (triggered by the D-002 `nature` bug — same class of error
  suspected elsewhere) found and fixed:
  - **Removed `valueShape` (scalar/compound/array).** It **restated** the contract's `Value` oneof — the
    same single-source-of-truth violation as the old `nature`. The value model is owned by CommonTongue
    (`core.proto` `Value`; per-affordance in the payload) and referenced, never pinned on a role here.
  - **Removed `surfaceType` (A/B/AB).** Cryptic single letters, and **derivable from `group`** (device
    groups = device-control surface; `deck_*` = deck-input; `pro_av` = both). Folded the meaning into
    `group`'s description; dropped the redundant axis.
  - **Renamed `unmappedFallback` → `accessibleFallback`** and struck all "degrade"/"degrades" wording
    (Palette shared this). "Degrade" framed the accessible rendering as a *lesser* one — backwards for
    an accessibility floor whose whole point is a **first-class, fully-operable** rendering. Best
    Practices + the Accessibility North Star: name it for what it is.
  - **Added `scripts/check-registry.py`** — enforces schema-conformance **and** referential integrity
    (every `accessibleFallback`/`gatedBy` resolves to a real role), which JSON Schema cannot express
    natively. Closes the unenforced-invariant gap (interface-stability: make it a mechanical gate over
    the schema, verified by attack — the negative control confirms a dangling fallback → exit 1).
  - **`$id`** changed from an invented `surfaceworks.dev` domain to the real, resolvable repo raw URL
    (Best Practice: `$id` should be a stable, dereferenceable absolute URI).
  - **`status` enum semantics** documented: `prototype` = close to final shape but consumers building
    against it (Lucidity, DeckLibre) may still force breaking changes; `stable` = owner-triggered
    additive-only-forever commitment. Everything stays `prototype` until the consumer apps are closer to
    done. (Values unchanged; description made honest — no bogus third value.)
- **Why:** all fixes trace to the same three lenses as D-002 — Correctness/SoT (don't restate contract
  facts; don't model a device fact as a role fact), Best Practices (idiomatic access vocab, resolvable
  `$id`, mechanical enforcement), and the Accessibility North Star (the fallback wording).
- **Provenance:** `[V]` — schema valid draft-2020-12; 196 roles revalidate after the field changes;
  `scripts/check-registry.py` passes; negative control confirms the integrity gate rejects a dangling
  fallback.

---

## Open items — do NOT build on these

### O-101 — Vocabulary is a prototype, not frozen
- **State:** open. `data/roles.json` `status: prototype` — the role set moves as Lucidity and other
  renderers build against it. Coverage target: standard 90%; the long tail is a product's own
  extension (`unmapped` or a vendor role).
- **Closes when:** the owner promotes the vocabulary to `stable` (a one-way cut the owner triggers,
  not the agent).
