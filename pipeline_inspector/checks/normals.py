"""Check 05 — Normal Consistency. Scaffold placeholder; returns PASS."""

from .. import models
from . import base

CHECK_ID = "05_normal_consistency"
CHECK_NAME = "Normal Consistency"
SEVERITY = models.Severity.BLOCKER


def run(inputs):
    return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY)
