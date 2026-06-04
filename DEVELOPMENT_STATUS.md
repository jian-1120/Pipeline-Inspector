# Development Status

Pipeline Inspector is currently in **Scaffold / Early Prototype** status.

This file describes project maturity before Blender add-on packaging tests. It does not define new product features or implementation behavior.

## Phase Status

| Phase | Status |
|---|---|
| Research | Complete |
| Evidence | Complete |
| MVP Definition | Complete |
| Architecture | Complete |
| Implementation Spec | Complete |
| Scaffold | Complete |
| Real Checks | Not complete |
| Blender Runtime Test | Not complete |

## Current Repository State

The repository contains an initial Blender add-on folder:

- `pipeline_inspector/`

The scaffold includes registration shell, panel/operator shell, scoring/report modules, and five placeholder check modules.

## Current Placeholder Checks

The current check modules exist as scaffold placeholders only:

1. Texture Presence
2. Material Assignment
3. Applied Scale
4. UV Existence
5. Normal Consistency

They do not yet perform real inspection logic and must not be used for real delivery decisions.

## Current Use

Suitable now:

- repository review
- zip packaging test
- Blender add-on load test
- registration sanity check

Not suitable now:

- real asset inspection
- client delivery decisions
- marketplace submission decisions
- production quality gates

## Gate Before Real Product Use

Pipeline Inspector cannot be considered usable until real checks are implemented and tested inside Blender runtime.
