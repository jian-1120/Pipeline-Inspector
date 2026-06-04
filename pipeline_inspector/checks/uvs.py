"""Check 04 — UV Existence. Scaffold placeholder; returns PASS."""

from .. import models
from . import base

CHECK_ID = "04_uv_existence"
CHECK_NAME = "UV Existence"
SEVERITY = models.Severity.BLOCKER


def run(inputs):
    return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY)
