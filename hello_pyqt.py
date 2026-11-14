
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QPushButton, QVBoxLayout
)

class HelloWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hello World - PyQt6")
        self.setGeometry(200, 200, 350, 200)

        self.label = QLabel("Welcome to PyQt6!")

        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.show_message)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def show_message(self):
        self.label.setText("Hello! Button Clicked.")

app = QApplication(sys.argv)
window = HelloWindow()
window.show()
sys.exit(app.exec())


