"""Check 03 — Applied Scale. Scaffold placeholder; returns PASS."""

from .. import models
from . import base

CHECK_ID = "03_applied_scale"
CHECK_NAME = "Applied Scale"
SEVERITY = models.Severity.BLOCKER


def run(inputs):
    return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY)
