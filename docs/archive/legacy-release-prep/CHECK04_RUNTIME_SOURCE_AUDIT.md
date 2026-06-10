# Check04 Runtime Source Audit

Date: 2026-06-09

Role: Runtime Operator

Purpose: determine exactly which `pipeline_inspector/checks/uvs.py` file Blender 5.1.1 is executing at runtime.

## Result

**B. Runtime loads stale placeholder code.**

Blender is not executing the latest repository implementation of Check04.

## Project Root Used

Current valid project root:

`C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector`

Requested comparison path:

`C:\Users\简某\Desktop\AI\PL总\Pipeline-Inspector`

Status:

- The requested `PL总` path does not exist on this machine.
- `PL总` was previously renamed to `Pipeline Inspector总`.
- The source comparison below uses the current valid project root.

## Blender Runtime Environment

- Blender executable: `D:\ProgramData\blender.exe`
- Blender version: `5.1.1`
- Blender Python version: `3.13.9`
- Runtime command mode: `blender --background --python <audit script>`

Blender script paths:

- `D:\ProgramData\5.1\scripts`
- `C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts`

Blender user add-ons path:

`C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons`

## Active Add-on Path

Blender loaded the add-on module from:

`C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector\__init__.py`

Runtime-loaded Check04 source path:

`C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector\checks\uvs.py`

Runtime-loaded file metadata:

- Size: `281` bytes
- Last modified: `2026-06-09 02:04:02`
- SHA256: `d0e333a416ecfb2902c3cb01460f2a3de7d7a0486bde80103a3d9ba94a210c72`

Runtime-loaded file content excerpt:

```python
"""Check 04 — UV Existence. Scaffold placeholder; returns PASS."""

from .. import models
from . import base

CHECK_ID = "04_uv_existence"
CHECK_NAME = "UV Existence"
SEVERITY = models.Severity.BLOCKER


def run(inputs):
    return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY)
```

Runtime markers:

- Contains placeholder phrase: yes
- Contains `def uv_status`: no
- Contains `def degenerate_active_status`: no
- Contains `no usable UV map` message: no
- Contains `base.make_fail`: no

## Repository Source Path

Current repository Check04 source:

`C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector\pipeline_inspector\checks\uvs.py`

Repository file metadata:

- Size: `4692` bytes
- Last modified: `2026-06-08 21:47:30`
- SHA256: `e0ee9e5da91c6101fd17d52addb699f415cdb838df369db57b5049481df3f42e`

Repository source content markers:

- Contains placeholder phrase: no
- Contains `def uv_status`: yes
- Contains `def degenerate_active_status`: yes
- Contains `no usable UV map` message: yes
- Contains `base.make_fail`: yes

Repository source excerpt:

```python
"""Check 04 — UV Existence.

FAILs any visible non-linked mesh object that has no UV map, or whose active
UV map exists but contains no UV data (BLOCKER). Additionally WARNs when a
mesh has multiple UV layers, its active layer is degenerate (collapsed to a
point), but a non-active layer carries usable UV data. Read-only.
"""

CHECK_ID = "04_uv_existence"
CHECK_NAME = "UV Existence"
SEVERITY = models.Severity.BLOCKER

_PASS_MESSAGE = "All mesh objects have UV maps."
_REASON_NO_MAP = "Object has no UV map."
_REASON_EMPTY_MAP = "UV map exists but contains no UV data."
```

## Diff Summary

Runtime-loaded `uvs.py`:

- Is a scaffold placeholder.
- Always returns `base.make_pass(...)`.
- Has no object UV inspection.
- Has no no-UV failure path.
- Has no empty-UV-data failure path.
- Has no degenerate-active warning path.
- Cannot list affected objects.

Repository `uvs.py`:

- Implements Check04 UV existence logic.
- Defines `uv_status(obj)`.
- Defines `degenerate_active_status(obj)`.
- Emits `base.make_fail(...)` for no usable UV maps.
- Emits warning for degenerate active UV layer with a usable alternate layer.
- Can report affected objects and issue records.

## Conclusion

Blender 5.1.1 is executing:

`C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector\checks\uvs.py`

That file is stale placeholder code, not the latest repository Check04 implementation.

Final answer:

**B. Runtime loads stale placeholder code.**
