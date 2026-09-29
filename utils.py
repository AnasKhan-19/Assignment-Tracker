from assignments import get_status

def get_statistics(assignments):
    total = len(assignments)
    completed = 0
    pending = 0
    overdue = 0

    for assignment in assignments:
        status = get_status(assignment)

        if status == "Completed":
            completed += 1
        elif status == "Overdue":
            overdue += 1
        else:
            pending += 1

    return total, completed, pending, overdue
