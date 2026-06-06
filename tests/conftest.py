"""Test config: stub a minimal `bpy` so bpy-free modules import outside Blender.

The package __init__ and ui modules import `bpy` at module load. The check
logic under test (transforms, base, scoring, report, models, constants) does
not touch bpy at runtime, so a lightweight stub is enough to let imports
resolve. No Blender behavior is simulated.
"""

import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def _install_bpy_stub():
    if "bpy" in sys.modules:
        return

    bpy = types.ModuleType("bpy")

    types_mod = types.ModuleType("bpy.types")
    types_mod.Operator = type("Operator", (), {})
    types_mod.Panel = type("Panel", (), {})

    utils_mod = types.ModuleType("bpy.utils")
    utils_mod.register_class = lambda cls: None
    utils_mod.unregister_class = lambda cls: None

    app_mod = types.SimpleNamespace(version_string="4.2.0")

    bpy.types = types_mod
    bpy.utils = utils_mod
    bpy.app = app_mod
    bpy.context = types.SimpleNamespace(scene=None)

    sys.modules["bpy"] = bpy
    sys.modules["bpy.types"] = types_mod
    sys.modules["bpy.utils"] = utils_mod


_install_bpy_stub()
