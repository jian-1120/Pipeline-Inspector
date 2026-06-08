"""Check 01 — Texture Presence. Scaffold placeholder; not implemented yet."""

from .. import models
from . import base

CHECK_ID = "01_texture_presence"
CHECK_NAME = "Texture Presence"
SEVERITY = models.Severity.BLOCKER


def run(inputs):
    return base.make_not_implemented(CHECK_ID, CHECK_NAME)
