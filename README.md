# Codex

**The family's control-role vocabulary.** Codex is the recommended, extensible catalog of cross-vendor
control *meanings* — `aperture`, `brightness`, `illuminance`, `pan`, `capture`, `macro_trigger`, and the
rest — the semantic keys a product tags its controls with so that renderers and aggregators understand
"the same control" the same way across brands. A **vocabulary, not code**.

Part of **SurfaceWorks**. The **CommonTongue** `SurfaceDescriptor` contract's `role` field is an **open
string** that merely *references* Codex — the contract does not depend on it. Align your roles to Codex for
whole-ecosystem interop (one aggregator controlling many brands) and for shared persona vocabulary; or use
`x.<vendor>.<name>` / `unmapped` and still render perfectly.

**Recommended, not required. Recommended core + add your own by PR.** "If you want interop with the whole
ecosystem, use these names; otherwise roll your own."

**Status:** prototype — seeded from a five-domain control-surface research sweep (lighting, light meters,
streaming/macro decks, virtual/touch surfaces, pro-AV/DAW/grading) plus CameraConductor's verified camera
vocabulary. See `docs/_working/reference/`.
