# Roadmap

This roadmap is intentionally restrained. It only covers the steps needed to move from scaffold to the first real delivery checks.

## Phase 1: Blender Load Test

Goal: confirm the `pipeline_inspector/` folder can be zipped, installed, enabled, and loaded by Blender without registration errors.

Success condition:

- add-on installs from zip
- add-on can be enabled
- panel/operator registration does not fail
- placeholder run path does not crash

## Phase 2: Applied Scale Real Check

Goal: replace the Applied Scale placeholder with the first real read-only check.

Success condition:

- visible local mesh objects are inspected
- unapplied scale is reported
- the check remains read-only

## Phase 3: UV Existence Check

Goal: implement the minimal UV existence check.

Success condition:

- visible local mesh objects are inspected
- missing or empty UV data is reported
- no UV quality, overlap, packing, or texel-density logic is added

## Phase 4: Material / Texture Checks

Goal: implement narrow material and texture delivery checks.

Success condition:

- assigned material presence is checked
- referenced image texture presence/reachability is checked
- no shader quality, PBR correctness, color-space policy, or texture-quality analysis is added

## Phase 5: Normal Warning Check

Goal: implement a conservative normal warning check.

Success condition:

- obvious normal consistency risks are reported as warnings
- the check remains conservative
- no broad mesh cleanup or repair behavior is added
