
"""PyQt6 interface for LOCK IN Task Manager."""

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import task_logic


class TaskManager(QMainWindow):

    def __init__(self):
        super().__init__()

        self.selected_task_id = None

        self.setWindowTitle(
            "LOCK IN - Task Manager | Tandin Zangmo"
        )
        self.resize(1100, 760)
        self.setMinimumSize(800, 600)

        self.apply_theme()
        self.create_menu_bar()
        self.create_ui()
        self.load_tasks()

    # ---------------- THEME ----------------

    def apply_theme(self):
        """Apply purple and lavender styling."""

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #F5F1FC;
                font-family: Arial;
                font-size: 13px;
                color: #302747;
            }

            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                background-color: white;
                border: 1px solid #D8C9EC;
                border-radius: 7px;
                padding: 7px;
            }

            QPushButton {
                background-color: #8060B5;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 9px 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #654497;
            }

            QPushButton:pressed {
                background-color: #51367D;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #D8C9EC;
                gridline-color: #E8E0F1;
                selection-background-color: #DCCCF2;
                selection-color: #302747;
            }

            QHeaderView::section {
                background-color: #8060B5;
                color: white;
                padding: 8px;
                border: none;
            }

            QMenuBar {
                background-color: #E9E0F5;
            }

            QMenuBar::item:selected,
            QMenu::item:selected {
                background-color: #D8C9EC;
            }

            QProgressBar {
                background-color: white;
                border: 1px solid #D8C9EC;
                border-radius: 6px;
                text-align: center;
                min-height: 18px;
            }

            QProgressBar::chunk {
                background-color: #8060B5;
                border-radius: 5px;
            }
        """)

    # ---------------- MENU BAR ----------------

    def create_menu_bar(self):
        """Create File and Help menus."""

        file_menu = self.menuBar().addMenu("File")

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        help_menu = self.menuBar().addMenu("Help")

        about_action = help_menu.addAction("About LOCK IN")
        about_action.triggered.connect(self.show_about)

    # ---------------- MAIN INTERFACE ----------------

    def create_ui(self):
        """Create the application interface."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 18, 20, 18)
        main_layout.setSpacing(12)

        # Application heading
        heading = QLabel("LOCK IN.")
        heading.setStyleSheet(
            "font-size: 32px; font-weight: bold; color: #8060B5;"
        )

        subtitle = QLabel(
            "Less scrolling, more doing. Get things done!"
        )

        main_layout.addWidget(heading)
        main_layout.addWidget(subtitle)

        # Task form
        form_layout = QGridLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(
            "Enter task name"
        )

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Enter description"
        )
        self.description_input.setMaximumHeight(65)

        self.category_input = QComboBox()
        self.category_input.addItems([
            "Study", "Personal", "Work", "Others"
        ])

        self.priority_input = QComboBox()
        self.priority_input.addItems([
            "High", "Medium", "Low"
        ])

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd MMM yyyy")
        self.date_input.setDate(QDate.currentDate())

        form_layout.addWidget(
            QLabel("Task Name:"), 0, 0
        )
        form_layout.addWidget(
            self.title_input, 0, 1
        )

        form_layout.addWidget(
            QLabel("Description:"), 1, 0
        )
        form_layout.addWidget(
            self.description_input, 1, 1
        )

        form_layout.addWidget(
            QLabel("Category:"), 2, 0
        )
        form_layout.addWidget(
            self.category_input, 2, 1
        )

        form_layout.addWidget(
            QLabel("Priority:"), 3, 0
        )
        form_layout.addWidget(
            self.priority_input, 3, 1
        )

        form_layout.addWidget(
            QLabel("Due Date:"), 4, 0
        )
        form_layout.addWidget(
            self.date_input, 4, 1
        )

        form_layout.setColumnStretch(1, 1)
        main_layout.addLayout(form_layout)

        # Action buttons
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Task")
        self.edit_button = QPushButton("Update Task")
        self.delete_button = QPushButton("Delete Task")
        self.complete_button = QPushButton("Toggle Complete")
        self.clear_button = QPushButton("Clear")

        self.add_button.clicked.connect(
            self.add_task
        )
        self.edit_button.clicked.connect(
            self.edit_task
        )
        self.delete_button.clicked.connect(
            self.delete_task
        )
        self.complete_button.clicked.connect(
            self.complete_task
        )
        self.clear_button.clicked.connect(
            self.clear_fields
        )

        for button in (
            self.add_button,
            self.edit_button,
            self.delete_button,
            self.complete_button,
            self.clear_button
        ):
            button_layout.addWidget(button)

        main_layout.addLayout(button_layout)

        # Search and priority filter
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by task, description or category..."
        )

        self.filter_input = QComboBox()
        self.filter_input.addItems([
            "All", "High", "Medium", "Low"
        ])

        search_layout.addWidget(self.search_input, 3)
        search_layout.addWidget(self.filter_input, 1)

        main_layout.addLayout(search_layout)

        self.search_input.textChanged.connect(
            self.load_tasks
        )

        self.filter_input.currentTextChanged.connect(
            self.load_tasks
        )

        # Task table
        self.table = QTableWidget(0, 7)

        self.table.setHorizontalHeaderLabels([
            "ID", "Task", "Description",
            "Category", "Priority", "Due Date", "Status"
        ])

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.setColumnWidth(0, 45)
        self.table.setColumnWidth(1, 170)
        self.table.setColumnWidth(2, 230)

        self.table.itemSelectionChanged.connect(
            self.load_selected_task
        )

        main_layout.addWidget(self.table, 1)

        # Progress bar
        self.progress_label = QLabel(
            "Your progress: 0% (0/0 completed)"
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        main_layout.addWidget(self.progress_label)
        main_layout.addWidget(self.progress_bar)

    # ---------------- INFORMATION DIALOG ----------------

    def show_about(self):
        QMessageBox.about(
            self,
            "About LOCK IN",
            "LOCK IN - Task Manager\n"
            "Developed by Tandin Zangmo\n"
            "A PyQt6 task manager with SQLite data storage."
        )

    def show_error(self, message):
        QMessageBox.warning(
            self,
            "Unable to complete action",
            message
        )

    # ---------------- DISPLAY TASKS ----------------

    def load_tasks(self, *_):
        """Display tasks using search and priority filters."""

        try:
            tasks = task_logic.show_tasks()

        except Exception as error:
            self.show_error(
                f"Could not load tasks. Details: {error}"
            )
            return

        search_text = (
            self.search_input.text().strip().casefold()
        )

        selected_priority = (
            self.filter_input.currentText()
        )

        filtered_tasks = []

        for task in tasks:

            searchable_text = " ".join(
                str(value or "") for value in task[1:4]
            ).casefold()

            matches_search = (
                search_text in searchable_text
            )

            matches_priority = (
                selected_priority == "All"
                or task[4] == selected_priority
            )

            if matches_search and matches_priority:
                filtered_tasks.append(task)

        self.table.setRowCount(len(filtered_tasks))

        for row_number, task in enumerate(filtered_tasks):

            for column_number, value in enumerate(task):

                item = QTableWidgetItem(
                    str(value if value is not None else "")
                )

                if column_number == 0:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                self.table.setItem(
                    row_number, column_number, item
                )

        self.update_progress(tasks)

    # ---------------- SELECT TASK ----------------

    def load_selected_task(self):
        """Load selected task information into the form."""

        row = self.table.currentRow()

        if row < 0:
            return

        try:
            task_id = int(
                self.table.item(row, 0).text()
            )

            task = task_logic.find_task(task_id)

            if task is None:
                self.show_error(
                    "The selected task no longer exists."
                )
                return

            self.selected_task_id = task[0]

            self.title_input.setText(task[1])
            self.description_input.setPlainText(
                task[2] or ""
            )

            self.category_input.setCurrentText(task[3])
            self.priority_input.setCurrentText(task[4])

            due_date = QDate.fromString(
                task[5], "yyyy-MM-dd"
            )

            if due_date.isValid():
                self.date_input.setDate(due_date)
            else:
                self.date_input.setDate(
                    QDate.currentDate()
                )

        except (ValueError, AttributeError, IndexError) as error:
            self.show_error(
                f"Could not load task. Details: {error}"
            )

    # ---------------- ADD TASK ----------------

    def add_task(self):
        """Add a new task after validation."""

        try:
            success, message = task_logic.create_task(
                self.title_input.text(),
                self.description_input.toPlainText(),
                self.category_input.currentText(),
                self.priority_input.currentText(),
                self.date_input.date().toString("yyyy-MM-dd")
            )

            if not success:
                self.show_error(message)
                return

            QMessageBox.information(
                self, "Success", message
            )

            self.clear_fields()
            self.load_tasks()

        except Exception as error:
            self.show_error(
                f"Could not add task. Details: {error}"
            )

    # ---------------- GET SELECTED TASK ID ----------------

    def selected_task(self):
        """Return selected task ID."""

        row = self.table.currentRow()

        if row < 0 or self.table.item(row, 0) is None:

            QMessageBox.warning(
                self,
                "No task selected",
                "Please select a task from the table first."
            )

            return None

        return int(self.table.item(row, 0).text())

    # ---------------- DELETE TASK ----------------

    def delete_task(self):
        """Delete a task after confirmation."""

        task_id = self.selected_task()

        if task_id is None:
            return

        answer = QMessageBox.question(
            self,
            "Confirm deletion",
            "Are you sure you want to delete this task?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:

            try:
                task_logic.remove_task(task_id)

                self.clear_fields()
                self.load_tasks()

            except Exception as error:
                self.show_error(
                    f"Could not delete task. Details: {error}"
                )

    # ---------------- COMPLETE TASK ----------------

    def complete_task(self):
        """Toggle between Pending and Completed."""

        task_id = self.selected_task()

        if task_id is None:
            return

        task = task_logic.find_task(task_id)

        if task is None:
            self.show_error(
                "The selected task could not be found."
            )
            return

        new_status = (
            "Pending"
            if task[6] == "Completed"
            else "Completed"
        )

        try:
            task_logic.complete_task(
                task_id, new_status
            )

            self.load_tasks()

        except Exception as error:
            self.show_error(
                f"Could not update status. Details: {error}"
            )

    # ---------------- EDIT TASK ----------------

    def edit_task(self):
        """Update the selected task."""

        task_id = self.selected_task_id

        if task_id is None:
            task_id = self.selected_task()

        if task_id is None:
            return

        try:
            success, message = task_logic.edit_task(
                task_id,
                self.title_input.text(),
                self.description_input.toPlainText(),
                self.category_input.currentText(),
                self.priority_input.currentText(),
                self.date_input.date().toString("yyyy-MM-dd")
            )

            if not success:
                self.show_error(message)
                return

            QMessageBox.information(
                self, "Success", message
            )

            self.clear_fields()
            self.load_tasks()

        except Exception as error:
            self.show_error(
                f"Could not update task. Details: {error}"
            )

    # ---------------- CLEAR FORM ----------------

    def clear_fields(self):
        """Clear all input fields."""

        self.selected_task_id = None

        self.table.clearSelection()

        self.title_input.clear()
        self.description_input.clear()

        self.category_input.setCurrentIndex(0)
        self.priority_input.setCurrentIndex(0)

        self.date_input.setDate(
            QDate.currentDate()
        )

        self.title_input.setFocus()

    # ---------------- PROGRESS BAR ----------------

    def update_progress(self, tasks):
        """Calculate task completion percentage."""

        total = len(tasks)

        completed = sum(
            1 for task in tasks
            if task[6] == "Completed"
        )

        percentage = (
            int((completed / total) * 100)
            if total else 0
        )

        self.progress_bar.setValue(percentage)

        self.progress_label.setText(
            f"Your progress: {percentage}% "
            f"({completed}/{total} completed)"
        )
