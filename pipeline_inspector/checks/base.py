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


def make_not_implemented(check_id, name, message="Not implemented yet — this check did not inspect anything."):
    """Build a NOT_IMPLEMENTED CheckResult for a scaffold placeholder.

    Severity is INFO so scoring.derive() never deducts for it, keeping the
    READY FOR DELIVERY verdict uninfluenced by checks that did not run.
    """
    return models.CheckResult(
        id=check_id,
        name=name,
        status=models.Status.NOT_IMPLEMENTED,
        severity=models.Severity.INFO,
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


def make_warning(check_id, name, message, object_names, issues):
    """Build a single WARNING CheckResult.

    Severity is fixed to WARNING; affected_objects is derived from
    object_names via dedupe_sort_cap so the stored list is always sorted
    and capped regardless of caller input.
    """
    capped, _ = dedupe_sort_cap(object_names)
    return models.CheckResult(
        id=check_id,
        name=name,
        status=models.Status.WARNING,
        severity=models.Severity.WARNING,
        message=message,
        affected_objects=capped,
        issues=issues,
    )
