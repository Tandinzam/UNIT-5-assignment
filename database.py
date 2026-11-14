
"""Database operations for LOCK IN Task Manager."""

import sqlite3
from pathlib import Path

# Store the database beside this Python file.
DB_PATH = Path(__file__).resolve().parent / "tasks.db"


def connect_db():
    """Connect to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    """Create the task table."""
    with connect_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                category TEXT DEFAULT 'Others',
                priority TEXT DEFAULT 'Medium',
                due_date TEXT DEFAULT '',
                status TEXT DEFAULT 'Pending'
            )
        """)


def add_task(title, description, category, priority, due_date):
    """Add a new task."""
    with connect_db() as connection:
        cursor = connection.execute("""
            INSERT INTO tasks
            (title, description, category, priority, due_date, status)
            VALUES (?, ?, ?, ?, ?, 'Pending')
        """, (title, description, category, priority, due_date))

        return cursor.lastrowid


def get_tasks():
    """Retrieve all tasks."""
    with connect_db() as connection:
        rows = connection.execute("""
            SELECT id, title, description, category,
                   priority, due_date, status
            FROM tasks
            ORDER BY id DESC
        """).fetchall()

        return [tuple(row) for row in rows]


def get_task(task_id):
    """Retrieve one task using its ID."""
    with connect_db() as connection:
        row = connection.execute("""
            SELECT id, title, description, category,
                   priority, due_date, status
            FROM tasks
            WHERE id = ?
        """, (task_id,)).fetchone()

        return tuple(row) if row else None


def delete_task(task_id):
    """Delete a task."""
    with connect_db() as connection:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        return cursor.rowcount > 0


def update_status(task_id, status):
    """Update task completion status."""
    with connect_db() as connection:
        cursor = connection.execute("""
            UPDATE tasks
            SET status = ?
            WHERE id = ?
        """, (status, task_id))

        return cursor.rowcount > 0


def update_task(task_id, title, description,
                category, priority, due_date):
    """Edit an existing task."""
    with connect_db() as connection:
        cursor = connection.execute("""
            UPDATE tasks
            SET title = ?,
                description = ?,
                category = ?,
                priority = ?,
                due_date = ?
            WHERE id = ?
        """, (
            title, description, category,
            priority, due_date, task_id
        ))

        return cursor.rowcount > 0
