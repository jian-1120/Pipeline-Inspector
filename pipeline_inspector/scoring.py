"""Pure score derivation. No bpy import. Per IMPLEMENTATION_SPEC_V1.md Section 4."""

from . import models


def derive(results):
    score = 100
    blocker_count = 0
    warning_count = 0

    for r in results:
        if r.status == models.Status.FAIL and r.severity == models.Severity.BLOCKER:
            score -= 15
            blocker_count += 1
        elif r.status == models.Status.FAIL and r.severity == models.Severity.WARNING:
            score -= 5
            warning_count += 1
        elif r.status == models.Status.WARNING:
            score -= 3
            warning_count += 1

    if blocker_count >= 5:
        score = min(score, 29)
    elif blocker_count >= 3:
        score = min(score, 49)

    score = max(0, min(100, score))

    if blocker_count > 0 or score < 70:
        verdict = models.Verdict.NOT_READY
    elif warning_count > 0:
        verdict = models.Verdict.READY_WITH_WARNINGS
    else:
        verdict = models.Verdict.READY

    return score, verdict, blocker_count, warning_count
