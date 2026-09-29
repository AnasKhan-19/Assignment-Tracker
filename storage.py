import os

FILE_NAME = "assignments.txt"

def load_assignments():
    assignments = []

    if not os.path.exists(FILE_NAME):
        return assignments

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")

                if len(parts) != 6:
                    continue

                assignments.append({
                    "title": parts[0],
                    "subject": parts[1],
                    "deadline": parts[2],
                    "priority": parts[3],
                    "status": parts[4],
                    "description": parts[5]
                })
    except OSError:
        return []

    return assignments

def save_assignments(assignments):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for assignment in assignments:
                line = "|".join([
                    assignment["title"],
                    assignment["subject"],
                    assignment["deadline"],
                    assignment["priority"],
                    assignment["status"],
                    assignment["description"]
                ])
                file.write(line + "\n")
        return True
    except OSError:
        return False
