"""Session-scoped holder for the latest InspectionResult. Cleared on unregister."""

_latest_result = None


def set_latest_result(result):
    global _latest_result
    _latest_result = result


def get_latest_result():
    return _latest_result


def clear():
    global _latest_result
    _latest_result = None
