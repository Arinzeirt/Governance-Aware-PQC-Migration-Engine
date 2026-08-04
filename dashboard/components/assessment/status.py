def readiness_percentage(completed, total):

    if total <= 0:
        return 0

    return int((completed / total) * 100)


def readiness_status(completed, total):

    if completed == 0:
        return {
            "label": "Not Started",
            "level": "warning",
        }

    if completed < total:
        return {
            "label": "Assessment In Progress",
            "level": "info",
        }

    return {
        "label": "Ready to Continue",
        "level": "success",
    }
