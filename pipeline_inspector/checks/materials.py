"""Check 02 — Material Assignment. Scaffold placeholder; not implemented yet."""

from .. import models
from . import base

CHECK_ID = "02_material_assignment"
CHECK_NAME = "Material Assignment"
SEVERITY = models.Severity.BLOCKER


def run(inputs):
    return base.make_not_implemented(CHECK_ID, CHECK_NAME)
