# Codex — Role Registry (PROTOTYPE)

**Status:** DRAFT / prototype. The recommended cross-vendor **role** vocabulary — the semantic *meaning* of
a control. Seeded from a 2026-07-19 five-domain control-surface research sweep (lighting control · light
meters · streaming/macro decks · virtual/touch surfaces · pro-AV/DAW/grading) + CameraConductor's verified
camera vocabulary.
**Recommended, not required · `lowercase_snake` (open-registry casing) · vendor tail `x.<vendor>.<name>` ·
grow by PR.** A product may use `unmapped` or a vendor role and still render. Coverage target: standard 90%;
the long tail is a product's own extension. **Nature** (coarse ROLE-level capability): `settable` = a
property a client sets · `readonly` = telemetry a client observes · `action` = a momentary thing a client
fires. **Nature does NOT state read-write vs write-only** — that is a per-*device* fact owned by the
**CommonTongue** descriptor (`PropertyPayload.Access` READ_ONLY / READ_WRITE / WRITE_ONLY, plus the value
`Confidence` axis CONFIRMED / COMMANDED for a write-only device). The same `settable` role is read-write on
a device that reports back and write-only on one that does not (e.g. a write-only fixture); Codex references
that axis, never restates it. A role's **`group`** implies its surface kind (`universal`/`lighting`/
`metering`/`camera` = device-control; `deck_affordance`/`deck_binding` = deck-input; `pro_av` = both).
**Cross-cutting contract implications** (compound/array value types, bidirectional binding, mode-gating, the
deck binding/action axis) live with the contract in **CommonTongue** (`docs/reference/`), which this
prototype was split out of.

**Authoritative artifact:** this document is **human narration**. The machine-readable, authoritative
form of the vocabulary is **[`data/roles.json`](../../data/roles.json)**, validated by
**[`schema/role-registry.schema.json`](../../schema/role-registry.schema.json)** (JSON Schema 2020-12).
Renderers (Lucidity and others) consume the data; grow the vocabulary by PR against the data (add an
entry — every entry must carry `group`, `nature`, and an `accessibleFallback`: the first-class accessible
role a renderer uses for an unrecognised role). Referential integrity (every `accessibleFallback`/`gatedBy`
resolves to a real role) is enforced by [`scripts/check-registry.py`](../../scripts/check-registry.py). The
form and its rationale are recorded in [`decision-log.md`](decision-log.md) (D-001, D-002, D-003). The
sections below narrate the same set the data holds; on any discrepancy, **the data is the source of truth**.

---

## 0. Universal (every device — the interop-load-bearing overlap)
`on_off` · `identify`(A) · `reset`(A) · `device_label` · `power_state` · `battery_level`(R) · `temperature`(R) ·
`connection_health`/`online`(R) · `signal_status`(R) · `device_status`/`error_flags`(R) · `firmware_version`(R)

## 1. Lighting control (A · write-dominant)
- **Intensity:** `intensity`(=dimmer) · `intensity_min`/`intensity_max` · `dimmer_curve` · `dimming_speed` · `pwm_frequency`
- **Shutter/strobe:** `shutter`(open/closed) · `strobe`(Hz) · `strobe_mode`
- **Colour** *(gated by `color_mode` ∈ hsi|cct|rgb(w)|xy|gel|cmy):* `hue` · `saturation` · `color_rgb`(compound) ·
  `red`/`green`/`blue` · `white`/`warm_white`/`cool_white` · `amber`/`lime`/`cyan`/`indigo`/`uv` · `color_xy`(compound) ·
  `color_temperature` · `tint` · `cmy_cyan`/`cmy_magenta`/`cmy_yellow` · `color_wheel` · `gel_select` · `color_preset`
- **Position:** `pan` · `tilt` (a `pan_tilt` compound) · `pan_tilt_speed` · `pan_continuous`/`tilt_continuous` · `pan_invert`/`tilt_invert`
- **Beam/optics:** `zoom` · `focus` · `iris` · `frost` · `framing_blade`(compound)
- **Effects:** `gobo_select` · `gobo_rotation` · `prism` · `prism_rotation` · `animation_wheel` · `effect_preset` · `effect_speed` · `sound_active`/`sound_sensitivity`
- **Config:** `fixture_mode`(personality) · `dmx_address` · `fan_mode`/`fan_speed` · `lamp_state`
- **Telemetry (R):** `lamp_hours` · `fan_rpm` · `voltage`/`current`/`power_draw`

## 2. Light metering (A · telemetry-dominant R + a few settings)
- **Exposure (R):** `illuminance` · `luminance` · `exposure_value` · `recommended_aperture`/`recommended_shutter`/`recommended_shutter_angle` ·
  `flash_percentage` · `flash_duration` · `exposure_ratio` · `analog_exposure_indicator` · `average_reading` · `highlight_reading`/`shadow_reading`
- **Colour (R):** `color_temperature` · `tint` · `chromaticity_xy`(compound) · `cri` · `cri_sample_values`(**array** R1–R15) · `tlci` ·
  `tm30_rf`/`tm30_rg` · `ssi` · `spectral_power_distribution`(**array**) · `dominant_wavelength` · `lb_index` · `filter_recommendation`
- **Settings (W):** `iso` · `metering_mode` · `priority_mode` · `still_cine_mode` · `frame_rate` · `shutter_angle_setting` ·
  `exposure_compensation` · `target_color_temperature` · `filter_system` · `illuminance_unit`/`luminance_unit`

## 3. Camera (A) — CameraConductor's `[V]` vocabulary
`aperture` · `shutter_speed` · `iso` · `exposure_compensation` · `exposure_program` · `metering_mode` · `white_balance`(compound) ·
`focus_mode` · `focus_area` · `focus_distance` · `af_trigger`(A) · `capture`(A) · `drive_mode` · `image_quality` · `live_view` ·
`ptz_pan`/`ptz_tilt`/`ptz_zoom`

## 4. Deck/input **affordance** types (B) — affordance *kinds*, not device meanings
`key` · `lcd_key` · `encoder` · `dial_with_press` · `fader` · `touch_strip` · `touchscreen_cell` · `pedal` · `button`
— carrying **press-phase** (`press`/`release`/`long_press`/`double_press`), **rotation** (`detented`|`endless`, `acceleration`),
and a **feedback channel** `rgb`|`lcd_bitmap`|`lcd_strip`|`led_ring`|`title`|`state`|`ok`|`alert`|`haptic`.
*Virtual/touch adds:* `button_momentary`/`button_toggle`/`button_trigger` · `pad` · `xy_pad` · `radial`/`radar` · `knob` ·
`encoder_relative` · `fader_relative` · `multi_fader` · `multi_slider` · `grid`/`matrix` · `range_slider` · `keyboard_piano` ·
`chord_trigger` · `label`/`text_display` · `meter` · `monitor`/`scope`.

## 5. Deck **binding/action** vocabulary (B) — the "what a control binds *to*" axis
`launch_app` · `open_url` · `hotkey` · `hotkey_switch` · `text_input` · `media_control` · `macro_trigger` ·
`multi_action`/`multi_action_switch` · `toggle`/`stateful` (N-steps model) · `scene_switch` · `source_toggle` · `page_switch` ·
`profile_switch` · `folder_open` · `volume_set`/`volume_adjust` · `value_adjust` · `scrub`/`jog` · `osc_send` · `midi_send` · `reset_value`.

## 6. Pro-AV distinctive (A+B — surface reflects host state *and* emits)
`motorized_fader`(bidirectional+touch) · `v_pot`(endless+ring) · `jog_wheel` · `shuttle_ring`(spring-return rate) · `t_bar`(transition) ·
`trackball`(compound X/Y+ring) · `control_ring` · `dve_joystick`(3-axis) · `transport_control`(cluster) · `bus_source_select`(radio+tally) ·
`transition_select`/`auto_cut` · `keyer_toggle` · `channel_mode_button`(mute/solo/rec_arm/select) · `bank_nav`/`channel_nav`;
**feedback-only:** `scribble_strip` · `channel_meter` · `timecode_display` · `soft_label`.
