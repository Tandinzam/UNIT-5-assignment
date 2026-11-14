
"""Main entry point for LOCK IN Task Manager."""

import sys
from PyQt6.QtWidgets import QApplication

import database
from ui import TaskManager


def main():
    # Create the database table if it does not exist.
    database.create_table()

    # Start the PyQt application.
    app = QApplication(sys.argv)
    app.setApplicationName("LOCK IN Task Manager")

    # Create and display the main window.
    window = TaskManager()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
