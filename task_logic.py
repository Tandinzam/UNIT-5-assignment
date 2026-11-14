
"""Application logic and validation for LOCK IN."""

import database

VALID_CATEGORIES = {
    "Study", "Personal", "Work", "Others"
}

VALID_PRIORITIES = {
    "High", "Medium", "Low"
}


def validate_task(title, category, priority):
    """Validate task information."""

    if not title or not title.strip():
        return False, "Please enter a task name."

    if len(title.strip()) > 100:
        return False, "Task name must be 100 characters or fewer."

    if category not in VALID_CATEGORIES:
        return False, "Please select a valid category."

    if priority not in VALID_PRIORITIES:
        return False, "Please select a valid priority."

    return True, "Valid task information."


def create_task(title, description,
                category, priority, due_date):
    """Validate and create a task."""

    valid, message = validate_task(
        title, category, priority
    )

    if not valid:
        return False, message

    database.add_task(
        title.strip(),
        description.strip(),
        category,
        priority,
        due_date
    )

    return True, "Task added successfully!"


def show_tasks():
    """Display all saved tasks."""
    return database.get_tasks()


def find_task(task_id):
    """Find a task using its ID."""
    return database.get_task(task_id)


def remove_task(task_id):
    """Remove a task."""
    return database.delete_task(task_id)


def complete_task(task_id, status):
    """Change task completion status."""

    if status not in {"Pending", "Completed"}:
        return False

    return database.update_status(task_id, status)


def edit_task(task_id, title, description,
              category, priority, due_date):
    """Validate and update an existing task."""

    valid, message = validate_task(
        title, category, priority
    )

    if not valid:
        return False, message

    updated = database.update_task(
        task_id,
        title.strip(),
        description.strip(),
        category,
        priority,
        due_date
    )

    if not updated:
        return False, "Selected task could not be found."

    return True, "Task updated successfully!"
