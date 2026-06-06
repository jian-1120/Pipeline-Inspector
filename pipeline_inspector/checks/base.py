"""Shared check helpers.

Real checks emit exactly one CheckResult per run (PASS or FAIL/WARNING),
never one per object. affected_objects is the deduplicated, alphabetically
sorted, capped projection of the per-object IssueRecord names.
"""

from .. import constants, models


def make_pass(check_id, name, severity, message="Placeholder PASS — check not yet implemented."):
    return models.CheckResult(
        id=check_id,
        name=name,
        status=models.Status.PASS,
        severity=severity,
        message=message,
    )


def dedupe_sort_cap(object_names):
    """Dedupe, sort alphabetically, and cap to AFFECTED_OBJECTS_CAP.

    Returns (capped_names, overflow_count). overflow_count is 0 when the
    deduplicated list fits within the cap.
    """
    unique = sorted(set(object_names))
    if len(unique) > constants.AFFECTED_OBJECTS_CAP:
        capped = unique[:constants.AFFECTED_OBJECTS_CAP]
        return capped, len(unique) - constants.AFFECTED_OBJECTS_CAP
    return unique, 0


def make_fail(check_id, name, severity, message, object_names, issues):
    """Build a single FAIL CheckResult.

    affected_objects is derived from object_names via dedupe_sort_cap so the
    stored list is always sorted and capped regardless of caller input.
    """
    capped, _ = dedupe_sort_cap(object_names)
    return models.CheckResult(
        id=check_id,
        name=name,
        status=models.Status.FAIL,
        severity=severity,
        message=message,
        affected_objects=capped,
        issues=issues,
    )
