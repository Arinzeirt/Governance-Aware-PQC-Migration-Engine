def assign_phase(item):

    priority = item.get("priority", "Low")

    if priority == "High":
        return "Phase 1"

    elif priority == "Medium":
        return "Phase 2"

    else:
        return "Phase 3"
