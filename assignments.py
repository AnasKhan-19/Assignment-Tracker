from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"

def create_assignment(title, subject, deadline, priority, description):
    return {
        "title": title.strip(),
        "subject": subject.strip(),
        "deadline": deadline.strip(),
        "priority": priority.strip(),
        "status": "Pending",
        "description": description.strip()
    }

def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, DATE_FORMAT)
        return True
    except ValueError:
        return False

def get_status(assignment):
    if assignment["status"] == "Completed":
        return "Completed"

    if not is_valid_date(assignment["deadline"]):
        return "Pending"

    deadline = datetime.strptime(
        assignment["deadline"], DATE_FORMAT
    ).date()

    if deadline < datetime.today().date():
        return "Overdue"

    return "Pending"

def search_assignments(assignments, keyword):
    keyword = keyword.lower().strip()

    if not keyword:
        return assignments

    results = []
    for assignment in assignments:
        if (keyword in assignment["title"].lower()
                or keyword in assignment["subject"].lower()):
            results.append(assignment)

    return results
