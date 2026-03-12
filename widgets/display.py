from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Display(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 20, 10, 10)

        # History linija
        self.history = QLineEdit()
        self.history.setReadOnly(True)
        self.history.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.history.setFixedHeight(30)
        self.history.setFont(QFont("Segoe UI", 13))  # ISPRAVLJENO
        self.history.setStyleSheet("""
            QLineEdit {
                color: #888888;
                border: none;
                padding-right: 5px;
                background: transparent;
            }
        """)

        # Glavni displej
        self.main = QLineEdit()
        self.main.setReadOnly(True)
        self.main.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main.setFixedHeight(70)
        self.main.setFont(QFont("Segoe UI", 48, QFont.Weight.Light))  # ISPRAVLJENO
        self.main.setText("0")
        self.main.setStyleSheet("""
            QLineEdit {
                border: none;
                padding-right: 5px;
                background: transparent;
            }
        """)

        layout.addWidget(self.history)
        layout.addWidget(self.main)

        self.setLayout(layout)

    def set_main(self, value):
        self.main.setText(str(value))

    def set_history(self, value):
        self.history.setText(value)

    def get_main(self):
        return self.main.text()