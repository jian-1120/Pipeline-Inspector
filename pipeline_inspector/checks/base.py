"""Shared check helpers. Scaffold phase: minimal PASS builder.

Real helpers (visibility filter, polycount cap, affected_objects dedupe)
land alongside the first real check implementation.
"""

from .. import models


def make_pass(check_id, name, severity, message="Placeholder PASS — check not yet implemented."):
    return models.CheckResult(
        id=check_id,
        name=name,
        status=models.Status.PASS,
        severity=severity,
        message=message,
    )
