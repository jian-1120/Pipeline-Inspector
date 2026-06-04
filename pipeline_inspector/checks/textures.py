"""Check 01 — Texture Presence. Scaffold placeholder; returns PASS."""

from .. import models
from . import base

CHECK_ID = "01_texture_presence"
CHECK_NAME = "Texture Presence"
SEVERITY = models.Severity.BLOCKER


def run(inputs):
    return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY)
